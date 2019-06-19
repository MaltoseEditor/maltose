import os.path
import re
import random
import time
import traceback
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .method import delete_blog, update_blog
from .customize.common import readfile
from .customize import cprint
from .settings import BLOG_PATH, PREVIEW_PORT, SOURCE_PATH, VERSION


def now():
    return time.strftime("[%m-%d %H:%M:%S]", time.localtime())


class MonitorFileEventHandler(FileSystemEventHandler):

    def on_modified(self, event):
        file = os.path.basename(event.src_path)
        if file.split(".")[-1] == "md":
            article = file.replace(".md", "")
            cprint.green(now(), end=" ")
            cprint.green(f"Update article {article}")
            try:
                update_blog(article)
            except:
                traceback.print_exc()

    def on_deleted(self, event):
        file = os.path.basename(event.src_path)
        if file.split(".")[-1] == "md":
            article = file.replace(".md", "")
            cprint.green(now(), end=" ")
            cprint.green(f"Delete article {article}")
            try:
                delete_blog(article)
            except:
                traceback.print_exc()


class MonitorFile:

    def __init__(self, path):
        self.observer = Observer()
        self.observer.schedule(MonitorFileEventHandler(), path, recursive=True)
        cprint.green(now(), end=" ")
        cprint.blue("Monitor path: " + SOURCE_PATH)

    def __del__(self):
        self.observer.stop()
        cprint.green(now(), end=" ")
        cprint.blue("Monitor stopped")

    def start(self):
        self.observer.start()


class Request(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.server_version = VERSION
        self.__slow_network = globals()["slow_network"]
        super().__init__(*args, **kwargs)

    def log_error(self, *args):
        pass  # Nothing to do

    def log_request(self, code='-', size='-'):
        if code == 200:
            cprint.green(now(), end=" ")
            cprint.blue("%s %s" % (self.requestline, str(code)))
        elif code == 302:
            cprint.warning(now(), end=" ")
            cprint.warning("%s %s" % (self.requestline, str(code)))
        elif code == 404:
            cprint.error(now(), end=" ")
            cprint.error("%s %s" % (self.requestline, str(code)))

    def __set_response_file_type(self, path):
        uri_suffix = path.split(".")[-1]
        uri_type = mimetypes.types_map.get("."+uri_suffix)
        if uri_type:
            return uri_type
        if uri_suffix == "woff2":
            return "font/woff2"
        return None

    # Handler for the GET requests
    def do_GET(self):
        if self.__slow_network:
            time.sleep(random.random() * 1)
        path = unquote(self.path)
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        if path[-1] == "/":
            path += "index.html"
        if path[0] == "/":
            path = path[1:]
        request_file = os.path.join(BLOG_PATH, path)
        try:
            page = readfile(request_file, True)
            self.send_response(200)
            self.send_header(
                'Content-Type', self.__set_response_file_type(path))
        except FileNotFoundError:
            try:
                page = readfile(os.path.join(BLOG_PATH, "404.html"), True)
            except FileNotFoundError:
                self.send_error(404)
                return
            self.send_response(404)
            self.send_header('Content-Type', "text/html")
        except PermissionError:
            self.send_response(302)
            self.send_header("Location", self.path + "/")
            page = b""

        # Send the html message
        page = re.sub(
            rb'<!--no-preview-->[\s\S]+?<!--no-preview-end-->', b"", page)

        self.send_header("Content-Length", len(page))
        self.send_header("Content-Encoding", "identity")
        self.end_headers()
        self.wfile.write(page + b"\r\n\r\n")
        return


class PreviewServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout = 1
        cprint.green(now(), end=" ")
        cprint.blue(f"Server running in http://127.0.0.1:{PREVIEW_PORT}")

    def __del__(self, *args, **kwargs):
        cprint.green(now(), end=" ")
        cprint.blue("Server stopped")

    def start(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            self.shutdown()


def main(*, isSlow=False):
    globals()["slow_network"] = isSlow
    monitor = MonitorFile(SOURCE_PATH)
    monitor.start()
    preview = PreviewServer(("0.0.0.0", PREVIEW_PORT), Request)
    preview.start()


if __name__ == '__main__':
    main()
