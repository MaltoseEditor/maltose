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
import re
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.urls import re_path
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.auth.decorators import login_required

from .views import coding_webhook, github_webhook, push

admin.site.site_header = 'Maltose | 后台管理'
admin.site.site_title = 'Maltose'
admin.site.index_title = 'Maltose'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('coding-webhook', coding_webhook),
    path('github-webhook', github_webhook),
    path('push', push),
    path('accounts/', include('django.contrib.auth.urls')),
    # 后台界面
    path('editor/', serve, kwargs={"path": 'index.html', "document_root": settings.EDITOR_ROOT}),
    re_path(r'^editor/(?P<path>.*)$', serve, kwargs={"document_root": settings.EDITOR_ROOT}),

    path('', include('maltose.article.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), serve,
                kwargs={"document_root": settings.STATICFILES_DIRS[0]}),
        re_path(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')), serve,
                kwargs={"document_root": settings.MEDIA_ROOT}),
    ]
