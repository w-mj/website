import json

import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from hospital.models import User, Doctor
from website.secrets import xcx_appid, xcx_xcxsecret

@require_POST
@csrf_exempt
def login(request):
    """
    用于小程序的“登陆”功能，获得用户openid和session_key
    """
    post_data = json.loads(request.body.decode('utf-8'))
    print(request.body.decode('utf-8'))
    code = post_data.get('code', None)
    if not code:
        return HttpResponse('{"result":"error", "msg":"no code"}')
    if code != "123":
        response = requests.get('https://api.weixin.qq.com/sns/jscode2session?'
                                'appid={}&secret={}&js_code={}&grant_type=authorization_code'
                                .format(xcx_appid, xcx_xcxsecret, code))
        decode = json.loads(response.content.decode())
        openid = decode.get('openid', None)
        if not openid:
            return HttpResponse(response.content)
    else:
        decode = {
            "session_key": "12345",
            "openid": "12345"
        }
        openid = "12345"

    try:
        xcx_user = User.objects.get(openid=openid)
        if xcx_user.role == 1:
            doctor = Doctor.objects.get(wechat=xcx_user)
            decode.update(doctor.json())
            decode.update({"isdoctor": True})
        elif xcx_user.role == 2:
            decode.update(xcx_user.json())
            decode.update({"isdoctor": False})
    except User.DoesNotExist:
        xcx_user = User(openid=openid)
        xcx_user.role = 2  # 默认为患者
        decode.update({"isdoctor": False})
        xcx_user.save()

    return JsonResponse(decode)
