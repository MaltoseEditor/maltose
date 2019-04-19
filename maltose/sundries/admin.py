from django.contrib import admin

from .models import *


@admin.register(FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
    pass
