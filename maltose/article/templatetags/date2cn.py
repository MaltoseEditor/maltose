"""
将日期转换为中国独有的日期称呼
"""
from django import template

register = template.Library()


"""
《尔雅 释天》：
    正月为陬
    二月为如
    三月为寎
    四月为余
    五月为皋
    六月为且
    七月为相
    八月为壮
    九月为玄
    十月为阳
    十一月为辜
    十二月为涂
"""
MONTH = [
    "陬",
    "如",
    "寎",
    "余",
    "皋",
    "且",
    "相",
    "壮",
    "玄",
    "阳",
    "辜",
    "涂"
]


@register.filter
def chinese_month(month):
    return MONTH[int(month) - 1]
