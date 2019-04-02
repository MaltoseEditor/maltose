from django.contrib import admin

from .models import *


class ReferenceAdmin(admin.TabularInline):
    model = Reference


class ImageAdmin(admin.TabularInline):
    model = Image


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ReferenceAdmin, ImageAdmin]
    list_display = ('title', 'create_time', 'update_time', 'is_draft', 'is_public')
    # list_editable = ('is_draft', 'is_public')
    fields = ('title', 'slug', 'corpus', 'tags')
    filter_horizontal = ('tags',)
    list_filter = ('is_draft', 'is_public')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Corpus)
class CorpusAdmin(admin.ModelAdmin):
    pass
