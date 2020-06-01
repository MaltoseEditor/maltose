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
月份 = ["", "陬", "如", "寎", "余", "皋", "且", "相", "壮", "玄", "阳", "辜", "涂"]

天干 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
地支 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戍", "亥"]


@register.filter
def chinese_month(month):
    return 月份[int(month)]


@register.filter
def chinese_year(year):
    """1984年为甲子年"""
    sub = int(year) - 1984
    return 天干[sub % 10] + 地支[sub % 12]
