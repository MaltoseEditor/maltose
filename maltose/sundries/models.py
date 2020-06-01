from django.db import models

__all__ = [
    "FriendLink",
]


class FriendLink(models.Model):
    name = models.CharField("名字", max_length=50)
    link = models.URLField("网址")

    def __str__(self):
        return self.name
