import datetime
import json

import requests
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from .models import ChatHistory
from website.settings import DEBUG
from website.secrets import amap_web_key, news_key, joke_key, turing_key, turing_userid


class CityMatch:
    def __init__(self):
        self.d = d = {'f': False}
        with open('chatbot/city.txt', encoding='utf-8') as f:
            for line in f:
                line = line[:-1]
                if len(line) < 2:
                    continue
                c = d
                for i, w in enumerate(line):
                    if w not in c:
                        c[w] = {'f': False}
                    c = c[w]
                    if i == len(line) - 1:
                        c['f'] = True

    def match(self, ob):
        c = self.d
        for w in ob:
            if w in c:
                c = c[w]
            else:
                return False
            if c['f'] is True:
                return True
        return c['f']


city_match = CityMatch()


def emo2emoji(emo):
    if 0 <= emo < 0.25:
        return "😩"
    if emo < 0.5:
        return "😭"
    if emo < 0.75:
        return "😊"
    if emo <= 1:
        return "😂"
    return ""


def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def reply(request, text, emo):
    if request.user.is_authenticated:
        history_item_response = ChatHistory()
        history_item_response.user = request.user
        history_item_response.is_response = True
        history_item_response.text = text
        history_item_response.save()
    return JsonResponse({"text": text, "emo": emo})


def news():
    while True:
        jsons = requests.get('http://v.juhe.cn/toutiao/index', {'key': news_key}).text
        json_obj = json.loads(jsons)
        if json_obj['reason'] != '成功的返回':
            yield "新闻服务器错误"
        if len(json_obj['result']['data']) == 0:
            yield "新闻服务器错误"
        for news in json_obj['result']['data']:
            yield '<a href="{}" target="_Blank">{}</a>'.format(news['url'], news['title'])


def joke():
    while True:
        jsons = requests.get('http://v.juhe.cn/joke/randJoke.php', {'key': joke_key}).text
        json_obj = json.loads(jsons)
        if json_obj['reason'] != 'success':
            yield "笑话服务器错误"
        for joke in json_obj['result']:
            yield joke['content']


news_getter = news()
joke_getter = joke()


def chat(request):
    if request.method == 'POST':
        text = request.POST.get("text")
        if text is None:
            return JsonResponse({"text": ""})

        emotion = requests.post('http://219.216.64.117:9091', data=text.encode(), timeout=10).text
        emotion = float(emotion)

        if request.user.is_authenticated:
            history_item = ChatHistory()
            history_item.user = request.user
            history_item.is_response = False
            history_item.text = text
            history_item.emotion = emotion
            history_item.save()

        if text is None or not text:
            return reply(request, "Inter Server Error.", emotion)

        if "天气" in text:
            t = weather(text)
            if t is not None:
                return reply(request, t, emotion)

        if '笑话' in text:
            return reply(request, next(joke_getter), emotion)

        if '新闻' in text:
            return reply(request, next(news_getter), emotion)

        if not check_contain_chinese(text):
            text = text.replace('@', '')
            text = text + "@" + emo2emoji(emotion)
            chat_result = requests.post('http://219.216.64.117:9093', data=text.encode('utf-8')).text
        else:
            request_data = {
                'perception': {
                    "inputText": {
                        "text": text
                    }
                },
                "userInfo": {
                    "apiKey": turing_key,
                    "userId": turing_userid
                }
            }
            request_result = requests.post('http://openapi.tuling123.com/openapi/api/v2',
                                           data=json.dumps(request_data)).text
            request_result = json.loads(request_result)
            if request_result['intent']['code'] != 10005:
                chat_result = 'internal server error.'
            result = []
            for r in request_result['results']:
                if r['resultType'] == 'text':
                    result.append(r['values']['text'])
            chat_result = '\n'.join(result)
        return reply(request, chat_result, emotion)

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
        except Exception as e:
            result = "Internal server error.\n" + str(e)
        return HttpResponse(result)
    return HttpResponseForbidden()


def sentiment(request):
    # if DEBUG:
    #     url = 'http://127.0.0.1:9091'
    # else:
    url = 'http://219.216.64.117:9091'
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


def synonym(request):
    url = 'http://219.216.64.117:9092'
    if request.method == 'GET':
        w1 = request.GET.get('w1', default='')
        w2 = request.GET.get('w2', default='')
        try:
            result = requests.post(url, data=(w1 + ' ' + w2).encode(), timeout=10).text
            print("R" + result)
        except Exception as e:
            result = "Internal server error.\n" + str(e)
        return HttpResponse(result)
    return HttpResponseForbidden()


def weather(text):
    text = text.strip()
    text = text.replace('天气', '')
    while text:
        if city_match.match(text):
            break
        text = text[1:]
    if not text:
        return None
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


def statistics(request):
    if request.method != 'GET':
        return HttpResponseForbidden()
    if not request.user.is_authenticated:
        return JsonResponse({})
    chat_history = ChatHistory.objects.filter(user=request.user, is_response=False)
    A = chat_history.filter(emotion__gte=0, emotion__lt=0.25).count()
    B = chat_history.filter(emotion__gte=0.25, emotion__lt=0.5).count()
    C = chat_history.filter(emotion__gte=0.5, emotion__lt=0.75).count()
    D = chat_history.filter(emotion__gte=0.75, emotion__lte=1).count()
    result = {
        'A': A,
        'B': B,
        'C': C,
        'D': D,
        'detail': [((x.time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"), x.emotion)
                   for x in chat_history if x.emotion >= 0]
    }
    return JsonResponse(result)
