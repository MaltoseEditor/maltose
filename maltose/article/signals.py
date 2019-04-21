import os

from django.db.models.signals import pre_delete, post_save, post_init
from django.dispatch import receiver
from django.conf import settings

from .models import Article, Image
from .build import update_all, update_feed, update_home, update_sitemap
from .build import update_article as update_a


@receiver(pre_delete, sender=Image)
def del_image(sender, instance, **kwargs):
    if str(instance.file):
        image = os.path.join(settings.MEDIA_ROOT, str(instance.file))
        if os.path.exists(image):
            os.remove(image)


@receiver(post_init, sender=Article)
def init_article(sender, instance, **kwargs):
    instance.onlychange_content = False


@receiver(post_save, sender=Article)
def update_article(sender, instance, **kwargs):
    if instance.onlychange_content:
        update_a(instance)
        update_home()
        update_feed()
        update_sitemap()
    else:
        update_all()


@receiver(pre_delete, sender=Article)
def delete_article(sender, instance, **kwargs):
    update_all()
