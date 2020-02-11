import json

import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from hospital.models import User, Doctor, Patient


@require_POST
@csrf_exempt
def login(request):
    """
    用于小程序的“登陆”功能，获得用户openid和session_key
    """
    post_data = json.loads(request.body.decode('utf-8'))
    print(request.body.decode('utf-8'))
    code = post_data.get('code', '')
    if not code:
        return HttpResponse('{"result":"error", "msg":"no code"}')
    response = requests.get('https://api.weixin.qq.com/sns/jscode2session?'
                            'appid={}&secret={}&js_code={}&grant_type=authorization_code'
                            .format(xcx_appid, xcx_appsecret, code))
    decode = json.loads(response.content.decode())
    openid = decode.get('openid', '')

    if not openid:
        print(response.content)
        parse_response = json.loads(response.content)
        decode['errcode'] = parse_response.get('errcode')
        decode['errmsg'] = parse_response.get('errmsg')
        avatar = post_data.get('avatarUrl', None)
        if avatar is None:
            return HttpResponse(response.content)
        openid = User.objects.get(avatar=avatar).openid
        decode['openid'] = openid

    try:
        xcx_user = User.objects.get(openid=openid)
        if xcx_user.role == 1:
            doctor = Doctor.objects.get(wechat=xcx_user)
            decode.update(doctor.info())
        elif xcx_user.role == 2:
            patient = Patient.objects.get(wechat=xcx_user)
            decode.update(patient.info())
    except User.DoesNotExist:
        xcx_user = User(openid=openid)
        xcx_user.save()

    print(json.dumps(decode))
    return JsonResponse(decode)
