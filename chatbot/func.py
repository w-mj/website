import json

import requests
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from .models import ChatHistory
from website.settings import DEBUG
from website.secrets import amap_web_key


def chat(request):
    if request.method == 'POST':
        text = request.POST.get("text")
        if text is None or not text:
            return JsonResponse({"text": "Inter Server Error."})
        if "天气" in text:
            return JsonResponse({"text": weather(text)})

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
    if DEBUG:
        url = 'http://127.0.0.1:9090'
    else:
        url = 'http://219.216.64.117:9090'
    if request.method == 'GET':
        text = request.GET.get('text', default='')
        if not text:
            return HttpResponse("请输入句子")
        try:
            result = requests.post(url, data=text.encode(), timeout=10).text
            print("R" + result)
        except Exception as e:
            result = "Internal server error.\n" + str(e)
        return HttpResponse(result)
    return HttpResponseForbidden()


def weather(text):
    text = text.strip()
    text = text.replace('天气', '')
    requests_data = {
        'key': amap_web_key,
        'address': text
    }
    requests_result = requests.get('https://restapi.amap.com/v3/geocode/geo', params=requests_data)
    result_json = json.loads(requests_result.text)
    if result_json['count'] == 0:
        return "天气服务器错误"
    adcode = result_json['geocodes'][0]['adcode']

    weather_data = {
        'key': amap_web_key,
        'city': adcode
    }
    weather_result = requests.get('https://restapi.amap.com/v3/weather/weatherInfo', params=weather_data)
    wd = json.loads(weather_result.text)['lives'][0]
    return "{}天气{}，温度{}℃，{}风{}级，湿度{}".format(
        wd['city'], wd['weather'], wd['temperature'],
        wd['winddirection'], wd['windpower'], wd['humidity']
    )
