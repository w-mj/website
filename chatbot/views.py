from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
import socket
import requests

from chatbot.ChatUser import ChatUser


def index(request):
    saved_id = request.COOKIES.get("uid", None)
    current_user = None
    if saved_id is not None:
        current_user = ChatUser()
    return render(request, 'index.html', {'current_user': current_user})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return JsonResponse({'result': 'success', 'msg':'123'})


def chat(request):
    if request.method == 'GET':
        token = request.GET.get("tk", default=0)
        text = request.GET.get("text", default="")
        if token != 0 and text:
            return JsonResponse({"text": text})
    return HttpResponse('error')


def separation(request):
    if request.method == 'GET':
        text = request.GET.get('text', default='')
        if not text:
            return HttpResponse("请输入句子")
        try:
            result = requests.post('http://127.0.0.1:9090', data=text.encode(), timeout=10).text
            print("R" + result)
        except Exception as e:
            result = "Internal server error.\n" + str(e)
        return HttpResponse(result)
    return HttpResponseForbidden()
