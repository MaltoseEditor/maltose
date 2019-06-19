import os
import re
import json

from src.datas.common import _copy_template, _delete_data_json, _update_data_json
from src.customize.common import join
from src.customize import cprint
from src.settings import BLOG_PATH, TEMPLATE_TIME


def index_time():
    time_path = join(BLOG_PATH, "time")
    time_list = []
    for year in os.listdir(time_path):
        if not os.path.isdir(join(time_path, year)):
            continue
        for month in os.listdir(join(time_path, year)):
            if not os.path.isdir(join(time_path, year, month)):
                continue
            with open(join(time_path, year, month, "index.json"), "r") as file:
                length = len(json.load(file))
            time_list.append({
                "name": f"{year}年{month}月",
                "link": f"time/{year}/{month}/",
                "count": length
            })
    with open(join(time_path, "index.json"), "w") as file:
        json.dump(time_list, file, indent=4)


def update_time(blog_info):
    if not blog_info["date"]:
        return
    cprint.green(f'Updating time {blog_info["date"]}', index=2)
    time_ = re.match(r"(?P<year>\d{4})-(?P<month>\d{2})", blog_info["date"])
    time_path = join(
        BLOG_PATH,
        "time",
        time_.group("year"),
        time_.group("month")
    )
    _copy_template(
        time_path,
        TEMPLATE_TIME,
        f"{time_.group('year')}年{time_.group('month')}月 | 时间"
    )
    _update_data_json(time_path, blog_info)


def delete_time(blog_info):
    if not blog_info["date"]:
        return
    cprint.green(f'Deleting time {blog_info["date"]}', index=2)
    time_ = re.match(r"(?P<year>\d{4})-(?P<month>\d{2})", blog_info["date"])
    time_path = join(
        BLOG_PATH,
        "time",
        time_.group("year"),
        time_.group("month")
    )
    _delete_data_json(time_path, blog_info)
