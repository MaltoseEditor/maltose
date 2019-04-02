"""maltose URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.views.static import serve as _serve

from .views import *


def serve(request, path):
    if path == "" or path[-1] == "/":
        path += 'index.html'
    return _serve(request, path, settings.BLOG_REPOSITORIES)


app_name = 'article'

urlpatterns = [
    path('', home, name='get_home'),
    path('articles/<str:slug>/', get_article, name="get_article"),
    path('tags/<str:name>/', get_tag, name="get_tag"),
    path('corpus/<str:name>/', get_corpus, name="get_corpus"),
    path('time/<int:year>/<int:month>/', get_time, name='get_time'),
    path('about/', about, name="get_about"),
    path('about/feedback.html', feedback, name="get_feedback"),
    path('about/donation.html', donation, name="get_donation"),
    path('404.html', page_not_found, name="get_404"),
    path('sitemap.xml', sitemap, kwargs={'sitemaps': {"article": Sitemap}}, name="get_sitemap"),
    path('feed.xml', Feed(), name="get_feed"),
    # 模型操作Api
    path('api/article/', ArticleView.as_view(), name='api_article'),
    path('api/tag/', TagView.as_view(), name='api_tag'),
    path('api/corpus/', CorpusView.as_view(), name='api_corpus'),
    path('api/reference/', ReferenceView.as_view(), name='api_reference'),
    path('api/image/', ImageView.as_view(), name='api_image'),
    # 使用Python渲染的Api
    path('api/render/', RenderView.as_view(), name="api_render"),

    # 在其他url规则无法匹配到时, 自动调用此函数模拟Github Page
    re_path(r'^(?P<path>.*)$', serve),
]
