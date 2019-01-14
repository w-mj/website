from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
import socket
import requests


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
