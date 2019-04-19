from .models import FriendLink


def get_all_friend(request):
    return {'friends': FriendLink.objects.all()}
