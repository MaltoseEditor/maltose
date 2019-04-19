import os

from django.db.models.signals import pre_delete, post_save, post_init
from django.dispatch import receiver
from django.conf import settings

from maltose.article.build import update_all

from .models import FriendLink


@receiver(post_save, sender=FriendLink)
def post_update_article(sender, instance, **kwargs):
    update_all()


@receiver(pre_delete, sender=FriendLink)
def delete_article(sender, instance, **kwargs):
    update_all()
