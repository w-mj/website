from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User


def signup(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username:
        return JsonResponse({'result': 'error', 'msg': 'no username'})
    if not password:
        return JsonResponse({'result': 'error', 'msg': 'no password'})
    query = User.objects.filter(username=username)
    if len(query) > 0:
        return JsonResponse({'result': 'error', 'msg': '该用户已经存在'})
    user = User.objects.create_user(username=username, password=password)
    return JsonResponse({'result': 'success', 'uid': user.id})


def signin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username:
        return JsonResponse({'result': 'error', 'msg': 'no username'})
    if not password:
        return JsonResponse({'result': 'error', 'msg': 'no password'})

    user = auth.authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({'result': 'error', 'msg': '用户名或密码错误'})
    auth.login(request, user)
    return JsonResponse({'result': 'success', 'uid': user.id})


def logout(request):
    auth.logout(request)
    return JsonResponse({'result': 'success'})


def changePsw(request):
    old_psw = request.POST.get('old_psw')
    new_psw = request.POST.get('new_psw')
    if not old_psw:
        return JsonResponse({'result': 'error', 'msg': 'no old password'})
    if not new_psw:
        return JsonResponse({'result': 'error', 'msg': 'no new password'})

    user = auth.authenticate(username=request.user.username, password=old_psw)
    if user is None:
        return JsonResponse({'result': 'error', 'msg': '旧密码错误'})
    user.set_password(new_psw)
    return JsonResponse({'result': 'success', 'uid': user.id})
