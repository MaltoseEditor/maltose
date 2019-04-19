import os

from django.db.models.signals import pre_delete, post_save, post_init
from django.dispatch import receiver
from django.conf import settings

from .models import Article, Image
from .build import update_all


@receiver(pre_delete, sender=Image)
def del_image(sender, instance, **kwargs):
    if str(instance.file):
        image = os.path.join(settings.MEDIA_ROOT, str(instance.file))
        if os.path.exists(image):
            os.remove(image)


@receiver(post_save, sender=Article)
def post_update_article(sender, instance, **kwargs):
    update_all()


@receiver(pre_delete, sender=Article)
def delete_article(sender, instance, **kwargs):
    update_all()
