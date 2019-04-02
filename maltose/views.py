import subprocess
import hmac
from hashlib import sha1

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


def push(request):
    subprocess.Popen('git pull && git add . && git commit -m "Auto commit by Maltose" && git push', cwd=settings.BLOG_REPOSITORIES, shell=True)
    return JsonResponse({"message": "success"})


@csrf_exempt
def coding_webhook(request):
    event = request.META.get("HTTP_X_CODING_EVENT")
    signature = request.META.get("HTTP_X_CODING_SIGNATURE", "").replace("sha1=", "")
    mac = hmac.new(settings.WEBHOOK_TOKEN.encode("ASCII"), msg=request.body, digestmod=sha1)
    if not hmac.compare_digest(str(mac.hexdigest()), str(signature)):
        return HttpResponseForbidden("What do you want to do?")
    if event == "ping":
        return JsonResponse({"message": "pong"})
    elif event == "push":
        subprocess.Popen("git pull", cwd=settings.BASE_DIR, shell=True)
    return JsonResponse({"message": "success"})


@csrf_exempt
def github_webhook(request):
    # TODO 完成Github-Webhook
    return HttpResponseForbidden("What do you want to do?")
