import requests
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from .models import ChatHistory


def chat(request):
    if request.method == 'POST':
        text = request.POST.get("text")
        if text is None or not text:
            return JsonResponse({"text": "Inter Server Error."})

        if request.user.is_authenticated:
            history_item = ChatHistory()
            history_item.user = request.user
            history_item.is_response = False
            history_item.text = text
            history_item.save()

            history_item_response = ChatHistory()
            history_item_response.user = request.user
            history_item_response.is_response = True
            history_item_response.text = text
            history_item_response.save()

        return JsonResponse({"text": text})

    return HttpResponseForbidden()


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
