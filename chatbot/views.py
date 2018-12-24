from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


def index(request):
    return render(request, 'index.html')


def chat(request):
    if request.method == 'GET':
        token = request.GET.get("tk", default=0)
        text = request.GET.get("text", default="")
        if token != 0 and text:
            return JsonResponse({"text": text})
    return HttpResponse('error')
