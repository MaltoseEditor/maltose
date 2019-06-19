import os
import re
import json
import shutil

from src.customize.common import join, readfile, writefile
from src.settings import BLOG_PATH, TEMPLATE_PATH


def _insert_json(datas: list, data: dict):
    """按时间顺序插入"""
    for i in range(len(datas) - 1, -1, -1):
        if datas[i]["date"] > data["date"]:
            datas.insert(i + 1, data)
            break
    else:
        datas.insert(0, data)
    return datas


def _copy_template(path: str, kind: str, title: str):
    """复制模板并且修改title"""
    if not os.path.exists(path):
        os.makedirs(path)

        page = readfile(join(TEMPLATE_PATH, f"{kind}.html"), encoding="UTF-8")
        page = re.sub(
            r"<title>[\s\S]*?</title>",
            f"<title>{title}</title>",
            page,
            count=1
        )
        writefile(join(path, "index.html"), page, encoding="UTF-8")


def _update_data_json(path: str, infos: dict):
    """更新或创建对应路径下的index.json文件"""
    path = join(path, "index.json")
    if os.path.exists(path):
        with open(path, "r+") as json_file:
            datas = json.load(json_file)
            for _, data in enumerate(datas):
                if data["title"] == infos["title"]:
                    data = infos
                    break
            else:
                datas = _insert_json(datas, infos)
            json_file.seek(0, 0)
            json_file.truncate()
            json.dump(datas, json_file, indent=4)
    else:
        with open(path, "w+") as json_file:
            json.dump([infos, ], json_file, indent=4)


def _delete_data_json(path: str, infos: dict):
    """删除对应目录下的对应信息"""
    with open(join(path, "index.json"), "r") as file:
        datas = json.load(file)
    with open(join(path, "index.json"), "w") as file:
        try:
            datas.remove(infos)
        except ValueError:
            pass
        if datas:
            json.dump(datas, file, indent=4)
        else:
            shutil.rmtree(path)
