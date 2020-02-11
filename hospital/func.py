import json
from datetime import datetime, timezone
from time import time

from django.http import HttpResponseNotFound, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .form import photoForm
from .models import *


def err(x):
    return JsonResponse({"error": "{}".format(x)})


@csrf_exempt
def picture(request):
    if request.method == 'POST':
        form = photoForm(request.POST, request.FILES)
        if 'img' in request.FILES:
            image = request.FILES["img"]
            image.name = str(time()) + image.name
            pic = Pictures()
            pic.pic = image
            pic.save()
            return JsonResponse({'img': pic.id})
        else:
            return err("upload image fail.")
    elif request.method == 'GET':
        if not request.GET.get('img'):
            return render(request, "hospital/index.html")
        try:
            img = Pictures.objects.get(id=request.GET.get('img', None))
        except Pictures.DoesNotExist:
            return HttpResponseNotFound()
        return HttpResponse(img.pic, content_type='image/png')

@csrf_exempt
def uploadill(request):
    try:
        post_data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return err("json data error.")
    must_contains = ['name', 'age', 'gender', 'ill', 'info', 'wechat']
    for x in must_contains:
        if x not in post_data:
            return err("no {}".format(x))
    wechat = User.objects.get(openid=post_data['wechat'])
    try:
        patient = Patient.objects.get(wechat=wechat)
    except Patient.DoesNotExist:
        patient = Patient()
        patient.wechat = wechat
        wechat.role = 2
        wechat.save()

    patient_fields = patient.json().keys()
    for x in patient_fields:
        if x in post_data and post_data[x] != getattr(patient, x):
            setattr(patient, x, post_data[x])
    patient.save()

    history = History()
    history.patient = patient
    history.ill = post_data['ill']
    history.info = post_data['info']
    history.doctor = None
    history.diag_time = None
    history.send_time = datetime.now()
    history.rank = 1
    history.save()

    if 'pics' in post_data:
        for pic in post_data['pics']:
            try:
                p = Pictures.objects.get(id=pic)
            except Pictures.DoesNotExist:
                return JsonResponse({'error': 'picture id {} does not exist.'.format(pic)})
            pt = PictureTable()
            pt.pic = p
            pt.history = history
            pt.save()

    return JsonResponse({'success': True})

@csrf_exempt
def checkcode(request):
    try:
        post_data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return err("json data error.")
    if 'code' not in post_data:
        return err("no code.")
    code = post_data['code']
    try:
        doctor = Doctor.objects.get(code=code)
    except Doctor.DoesNotExist:
        return err("invalid code")
    token = str(uuid.uuid4())
    doctor.token = token
    doctor.save()
    return JsonResponse({"code": code, "token": token})

@csrf_exempt
def doctor_signup(request):
    try:
        post_data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return err("json data error.")
    if 'did' not in post_data:
        return err("no doctor id")
    if 'token' not in post_data:
        return err("no token")
    try:
        doctor = Doctor.objects.get(did=post_data['did'])
    except Doctor.DoesNotExist:
        return err("invalid doctor id")
    if doctor.token != post_data['token']:
        return err("invalid token or doctor id")
    if 'wechat' not in post_data:
        return err("no wechat")
    try:
        wechat = User.objects.get(openid=post_data['wechat'])
        wechat.role = 1
    except User.DoesNotExist:
        return err("invalid wechat openid")
    doctor.wechat = wechat
    wechat.save()
    must_contains = ['name', 'gender', 'rank']
    for x in must_contains:
        if x not in post_data:
            return err("no {}".format(x))
        setattr(doctor, x, post_data[x])
    doctor.save()
    return JsonResponse({"success": True})


def get_patients(request):
    if 'did' not in request.GET:
        return err("no doctor id")
    did = request.GET['did']
    if did == 'all':
        patients = History.objects.all()
    else:
        try:
            doctor = Doctor.objects.get(did=did)
        except Doctor.DoesNotExist:
            return err("invalid doctor id")
        rank = doctor.rank
        patients = History.objects.filter(rank=rank, doctor=None)
    return JsonResponse({"patients": [x.json() for x in patients]})

@csrf_exempt
def start_diagnosis(request):
    try:
        post_data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return err("json data error.")
    if 'hid' not in post_data:
        return err("no history id")
    if 'did' not in post_data:
        return err("no doctor id")
    try:
        doctor = Doctor.objects.get(did=post_data['did'])
        history = History.objects.get(id=post_data['hid'])
        if history.doctor is not None:
            return err("this diagnosis is already started")
        doctor.credits += 1
        doctor.save()
        accept = Accept()
        accept.doctor = doctor
        accept.history = history
        accept.finish = False
        accept.save()
        history.doctor = doctor
        history.diag_time = datetime.now(tz=timezone.utc)
        history.save()
    except Doctor.DoesNotExist:
        return err("invalid doctor id")
    except History.DoesNotExist:
        return err("invalid history id")
    return JsonResponse({"success": True})


@csrf_exempt
def finish_diagnosis(request):
    try:
        post_data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return err("json data error.")
    if 'hid' not in post_data:
        return err("no history id")
    if 'did' not in post_data:
        return err("no doctor id")
    try:
        doctor = Doctor.objects.get(did=post_data['did'])
        history = History.objects.get(id=post_data['hid'])
        accept = Accept.objects.get(doctor=doctor, history=history)
        if accept.finish:
            return err("this diagnosis is already finish")
        doctor.credits += 2
        doctor.save()
        accept.finish = True
        accept.save()
    except Doctor.DoesNotExist:
        return err("invalid doctor id")
    except History.DoesNotExist:
        return err("invalid history id")
    except Accept.DoesNotExist:
        return err("the diagnosis isn't start")
    return JsonResponse({"success": True})


@csrf_exempt
def rank_up_history(request):
    try:
        post_data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return err("json data error.")
    if 'hid' not in post_data:
        return err("no history id")
    if 'did' not in post_data:
        return err("no doctor id")
    try:
        history = History.objects.get(id=post_data['hid'])
        doctor = Doctor.objects.get(did=post_data['did'])
        if history.rank < 3:
            history.rank += 1
        history.save()
        record = RankUPHistory()
        record.doctor = doctor
        record.history = history
        record.save()
    except History.DoesNotExist:
        return err("invalid history id")
    except Doctor.DoesNotExist:
        return err("invalid doctor id")
    return JsonResponse({"success": True})


def get_patient_history(pid):
    try:
        patient = Patient.objects.get(pid=pid)
        histories = History.objects.filter(patient=patient)
        return JsonResponse({"histories": [x.json() for x in histories]})
    except Patient.DoesNotExist:
        return err("invalid patient id")


def get_doctor_history(did):
    try:
        doctor = Doctor.objects.get(did=did)
        histories = Accept.objects.filter(doctor=doctor)
        return JsonResponse({"histories": [x.history.json() for x in histories]})
    except Doctor.DoesNotExist:
        return err("invalid doctor id")


def history(request):
    if request.GET.get('pid', None):
        return get_patient_history(request.GET['pid'])
    if request.GET.get('did', None):
        return get_doctor_history(request.GET['did'])
    return err("no patient id or doctor id")
