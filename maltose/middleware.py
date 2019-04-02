from django.http import HttpResponseBadRequest
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class RequestHostMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if settings.DEBUG and request.get_host() == "testserver":
            request.META['HTTP_HOST'] = settings.HOMEPAGE.split("://")[1].split("/")[0]
