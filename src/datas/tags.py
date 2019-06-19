import os
import json

from src.datas.common import _copy_template, _delete_data_json, _update_data_json
from src.customize.common import join
from src.customize import cprint
from src.settings import BLOG_PATH, TEMPLATE_TAG


def index_tags():
    tags_path = join(BLOG_PATH, "tags")
    tags_list = []
    for tag in os.listdir(tags_path):
        if not os.path.isdir(join(tags_path, tag)):
            continue
        with open(join(tags_path, tag, "index.json"), "r") as file:
            length = len(json.load(file))
        tags_list.append({
            "name": tag,
            "link": f"tags/{tag}/",
            "count": length
        })
    with open(join(tags_path, "index.json"), "w") as file:
        json.dump(tags_list, file, indent=4)


def update_tags(blog_info):
    if not blog_info["tags"]:
        return
    cprint.green(f'Updating tags {",".join(blog_info["tags"])}', index=2)
    for tag in blog_info["tags"]:
        tag_path = join(BLOG_PATH, "tags", tag)
        _copy_template(tag_path, TEMPLATE_TAG, f"{tag} | 标签")
        _update_data_json(tag_path, blog_info)


def delete_tags(blog_info):
    if not blog_info["tags"]:
        return
    cprint.green(f'Deleting tags {",".join(blog_info["tags"])}', index=2)
    for tag in blog_info["tags"]:
        tag_path = join(BLOG_PATH, "tags", tag)
        _delete_data_json(tag_path, blog_info)
