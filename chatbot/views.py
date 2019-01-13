from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import socket


def index(request):
    if socket.gethostname() == 'DESKTOP-589NS7B':
        server_url = 'http://127.0.0.1:8000/chat'
    else:
        server_url = 'http://fun.alphamj.cn/chat'
    return render(request, 'index.html', {'server_url': server_url})


def chat(request):
    if request.method == 'GET':
        token = request.GET.get("tk", default=0)
        text = request.GET.get("text", default="")
        if token != 0 and text:
            return JsonResponse({"text": text})
    return HttpResponse('error')
