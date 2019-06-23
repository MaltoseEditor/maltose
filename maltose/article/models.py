from django.db import models
from django.conf import settings
from django.urls import reverse

from maltose.maltose.models import ModelSerializationMixin

__all__ = (
    "Tag", 'Corpus', 'Article', 'Reference', 'Image'
)


class Tag(models.Model, ModelSerializationMixin):
    name = models.CharField("标签名", max_length=20, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/tags/{self.name}/'


class Corpus(models.Model, ModelSerializationMixin):
    name = models.CharField("文集名", max_length=20, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/corpus/{self.name}/'


class Article(models.Model, ModelSerializationMixin):
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    title = models.CharField("标题", max_length=25, unique=True)
    slug = models.SlugField("自定义链接", unique=True)
    # 由前端进行Markdown渲染, 能保证显示的及时性并减少服务器压力
    # source存在的意义仅为储存原始的markdown内容, 页面中应直接使用body
    source = models.TextField("Markdown", blank=True)
    body = models.TextField("文章内容", blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    corpus = models.ForeignKey(Corpus, on_delete=models.SET_NULL, blank=True, null=True)

    has_timeliness = models.BooleanField("具有时效性", default=False)
    is_draft = models.BooleanField("暂不发表", default=True)
    is_public = models.BooleanField("全部公开", default=True)

    @staticmethod
    def all():
        return Article.objects.filter(is_public=True, is_draft=False)

    def get_absolute_url(self):
        return reverse('article:get_article', kwargs={"slug": self.slug})

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.title


class Reference(models.Model, ModelSerializationMixin):
    name = models.CharField("名称", max_length=50)
    link = models.URLField("链接")
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.link


class Image(models.Model, ModelSerializationMixin):
    file = models.ImageField("路径", upload_to='')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.file)
