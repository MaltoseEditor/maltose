import os
import json

from src.datas.common import _copy_template, _delete_data_json, _update_data_json
from src.customize.common import join
from src.customize import cprint
from src.settings import BLOG_PATH, TEMPLATE_CORPUS


def index_corpus():
    corpus_path = join(BLOG_PATH, "corpus")
    corpus_list = []
    for corpus in os.listdir(corpus_path):
        if not os.path.isdir(join(corpus_path, corpus)):
            continue
        with open(join(corpus_path, corpus, "index.json"), "r") as file:
            length = len(json.load(file))
        corpus_list.append({
            "name": corpus,
            "link": f"corpus/{corpus}/",
            "count": length
        })
    with open(join(corpus_path, "index.json"), "w") as file:
        json.dump(corpus_list, file, indent=4)


def update_corpus(blog_info):
    corpus = blog_info["corpus"]
    if not corpus:
        return
    cprint.green(f'Updating corpus {blog_info["corpus"]}', index=2)
    corpus_path = join(BLOG_PATH, "corpus", corpus)
    _copy_template(corpus_path, TEMPLATE_CORPUS, f"{corpus} | 文集")
    _update_data_json(corpus_path, blog_info)


def delete_corpus(blog_info):
    corpus = blog_info["corpus"]
    if not corpus:
        return
    cprint.green(f'Deleting corpus {blog_info["corpus"]}', index=2)
    corpus_path = join(BLOG_PATH, "corpus", corpus)
    _delete_data_json(corpus_path, blog_info)
