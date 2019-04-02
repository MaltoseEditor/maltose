from django.conf import settings


def get_debug(request):
    host = settings.HOMEPAGE.split("://")[1].split("/")[0]
    if request.get_host() != host:
        return {"debug": True}
    else:
        return {"debug": False}
