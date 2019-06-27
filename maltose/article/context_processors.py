from django.db.models import Count, F
from django.db.models.functions.datetime import TruncMonth
from django.conf import settings

from .models import Corpus, Tag, Article


def get_all_corpus(request):
    corpuses = Article.visible().annotate(name=F('corpus__name')).values("name").distinct(). \
        annotate(count=Count('id')).values('name', 'count').order_by().filter(corpus__name__isnull=False)
    return {"corpuses": corpuses}


def get_all_tag(request):
    tags = Article.visible().annotate(name=F('tags__name')).values("name").distinct(). \
        annotate(count=Count('id')).values('name', 'count').order_by().filter(tags__isnull=False)
    return {"tags": tags}


def get_all_timelist(request):
    # 这里为啥要先用一个order_by()
    # 详见 https://stackoverflow.com/questions/45630801/django-orm-queryset-group-by-month-week-truncmonth
    time_list = Article.visible().annotate(date=TruncMonth('create_time')).values('date').distinct() \
        .annotate(count=Count('id')).values('date', 'count').order_by().order_by('-date')
    return {"time_list": time_list}
