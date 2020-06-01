import subprocess

from django.conf import settings


def create_dict(local=None, field=None, **kwargs):
    """
    以字典的形式从局部变量locals()中获取指定的变量

    :param local: dict
    :param field: str[] 指定需要从local中读取的变量名称
    :param kwargs: 需要将变量指定额外名称时使用
    :return: dict
    """
    if field is None or local is None:
        return {}
    result = {k: v for k, v in local.items() if k in field}
    result.update(**kwargs)
    return result


def push():
    """推送生成的静态页面到远程仓库"""
    return subprocess.Popen(
        'git pull && git add . && git commit -m "Auto commit by Maltose" && git push',
        cwd=settings.BLOG_REPOSITORIES,
        shell=True,
    )
