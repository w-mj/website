import json
from datetime import datetime, timezone
from time import time
from collections import Counter

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count
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
    must_contains = ['ill', 'info', 'wechat']
    for x in must_contains:
        if x not in post_data:
            return err("no {}".format(x))
    try:
        patient = User.objects.get(openid=post_data['wechat'])
    except User.DoesNotExist:
        return err("invalid wechat openid")

    his = History()
    his.patient = patient
    his.ill = post_data['ill']
    his.info = post_data['info']
    his.doctor = None
    his.diag_time = None
    his.send_time = datetime.now(tz=timezone.utc)
    his.rank = 1
    his.save()

    if 'pics' in post_data:
        for pic in post_data['pics']:
            try:
                p = Pictures.objects.get(id=pic)
            except Pictures.DoesNotExist:
                return JsonResponse({'error': 'picture id {} does not exist.'.format(pic)})
            pt = PictureTable()
            pt.pic = p
            pt.history = his
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
    if 'wechat' not in post_data:
        return err("no wechat")
    code = post_data['code']
    try:
        doctor = Doctor.objects.get(code=code)
        user = User.objects.get(openid=post_data['wechat'])
        user.role = 1
        user.save()
        doctor.wechat = user
        doctor.save()
    except Doctor.DoesNotExist:
        return err("invalid code")
    except User.DoesNotExist:
        return err("invalid wechat")

    return JsonResponse({"success": True})


@csrf_exempt
def doctor_signup(request):
    try:
        post_data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return err("json data error.")
    if 'wechat' not in post_data:
        return err("no wechat")

    try:
        user = User.objects.get(openid=post_data['wechat'])
        fields = ['name', 'gender', 'age', 'location', 'phone']
        for x in fields:
            if x in post_data:
                setattr(user, x, post_data[x])
        user.save()
    except User.DoesNotExist:
        return err("invalid wechat")

    return JsonResponse({"success": True})


def get_patients(request):
    if 'did' not in request.GET:
        return err("no doctor id")
    did = request.GET['did']
    if did == 'all':
        patients = History.objects.all()
    else:
        try:
            user = User.objects.get(openid=did)
            doctor = Doctor.objects.get(wechat=user)
        except User.DoesNotExist:
            return err("invalid doctor openid")
        except Doctor.DoesNotExist:
            return err("id={} is not a doctor".format(did))

        rank = doctor.rank
        patients = History.objects.filter(rank=rank, doctor=None).order_by('-send_time')
    page = request.GET.get('page', 1)
    try:
        patients = Paginator(patients, 10).page(page)
    except EmptyPage:
        patients = []
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
        doctor_user = User.objects.get(openid=post_data['did'])
        doctor = Doctor.objects.get(wechat=doctor_user)
        his = History.objects.get(id=post_data['hid'])
        if his.doctor is not None:
            return err("this diagnosis is already started")
        doctor.credits += 1
        doctor.save()
        accept = Accept()
        accept.doctor = doctor
        accept.history = his
        accept.finish = False
        accept.save()
        his.doctor = doctor
        his.diag_time = datetime.now(tz=timezone.utc)
        his.save()
    except User.DoesNotExist:
        return err("invalid doctor id")
    except Doctor.DoesNotExist:
        return err("{} is not a doctor".format(post_data['did']))
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
        doctor_user = User.objects.get(openid=post_data['did'])
        doctor = Doctor.objects.get(wechat=doctor_user)
        history = History.objects.get(id=post_data['hid'])
        accept = Accept.objects.get(doctor=doctor, history=history)
        if accept.finish:
            return err("this diagnosis is already finish")
        doctor.credits += 2
        doctor.save()
        accept.finish = True
        accept.save()
    except User.DoesNotExist:
        return err("invalid doctor id")
    except Doctor.DoesNotExist:
        return err("{} is not a doctor".format(post_data['did']))
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
        doc_user = User.objects.get(openid=post_data['did'])
        doctor = Doctor.objects.get(wechat=doc_user)
        if history.rank < 3:
            history.rank += 1
        history.save()
        record = RankUPHistory()
        record.doctor = doctor
        record.history = history
        record.save()
    except History.DoesNotExist:
        return err("invalid history id")
    except User.DoesNotExist:
        return err("invalid doctor id")
    except Doctor.DoesNotExist:
        return err("{} is not a doctor".format(post_data['did']))
    return JsonResponse({"success": True})


def get_patient_history(pid, page):
    try:
        patient = User.objects.get(openid=pid)
        histories = History.objects.filter(patient=patient).order_by("-send_time")
        try:
            histories = Paginator(histories, 10).page(page)
        except EmptyPage:
            histories = []
        return JsonResponse({"histories": [x.json() for x in histories]})
    except User.DoesNotExist:
        return err("invalid patient id")


def get_doctor_history(did, page):
    try:
        doc_user = User.objects.get(openid=did)
        doctor = Doctor.objects.get(wechat=doc_user)
        histories = Accept.objects.filter(doctor=doctor).order_by("-send_time")
        try:
            histories = Paginator(histories, 10).page(page)
        except EmptyPage:
            histories = []
        return JsonResponse({"histories": [dict(x.history.json(), **{'state': x.finish}) for x in histories]})
    except Doctor.DoesNotExist:
        return err("{} is not a doctor".format(did))
    except User.DoesNotExist:
        return err("invalid doctor id")


def history(request):
    page = request.GET.get('page', 1)
    if request.GET.get('pid', None):
        return get_patient_history(request.GET['pid'], page)
    if request.GET.get('did', None):
        return get_doctor_history(request.GET['did'], page)
    return err("no patient id or doctor id")


@csrf_exempt
def add_doctor(request):
    try:
        post_data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return err("json data error.")
    if 'did' not in post_data:
        return err("no doctor id")
    if 'code' not in post_data:
        return err("no code")

    fields = ['rank', 'code', 'did']
    doctor = Doctor()
    for x in fields:
        if x in post_data:
            setattr(doctor, x, post_data[x])
    doctor.save()
    return JsonResponse({"success": True})


def statistic(request):
    if 'did' not in request.GET:
        return err("no doctor id")
    did = request.GET['did']
    try:
        doc_user = User.objects.get(openid=did)
        me = Doctor.objects.get(wechat=doc_user)
    except User.DoesNotExist:
        return err("invalid doctor id")
    except Doctor.DoesNotExist:
        return err("{} is not a doctor".format(did))
    myacc = Accept.objects.filter(doctor=me).order_by("-id")
    mycured = myacc.count()
    dates = [x.history.diag_time for x in myacc]
    dates = [x.strftime("%Y-%m-%d") for x in dates]
    count = Counter(dates)
    if len(count) == 0:
        timedata = []
        dailycured = []
    else:
        (timedata, dailycured) = zip(*dict(count).items())
    timedata = timedata[0: 7] if len(timedata) > 7 else timedata
    dailycured = dailycured[0: 7] if len(dailycured) > 7 else dailycured

    doccured = Accept.objects.values("doctor").annotate(dcount=Count("doctor"))
    doccured = {x['doctor']: x['dcount'] for x in doccured}
    dname = [(x.id, x.wechat.name if x.wechat else "医生未填写个人信息") for x in Doctor.objects.all()]
    doccured = {x[1]: doccured.get(x[0], 0) for x in dname}
    doccured = doccured.items()
    doccured = sorted(doccured, key=lambda x: x[1], reverse=True)
    (docname, totalcured) = zip(*doccured)
    myseat = doccured.index((me.wechat .name if me.wechat else "医生未填写个人信息", mycured)) + 1
    return JsonResponse(
        {"timedata": timedata, "dailycured": dailycured,
         "docname": docname, "totalcured": totalcured,
         "mycured": mycured, "myseat": myseat, "myscore": me.credits
         })


def patient_detail(request):
    pid = request.GET.get('pid', None)
    if pid is None:
        return err("no pid")
    try:
        user = User.objects.get(openid=pid)
        return JsonResponse(user.json())
    except User.DoesNotExist:
        return err("invalid pid")


def history_detail(request):
    hid = request.GET.get('hid', None)
    if hid is None:
        return err("no hid")
    try:
        his = History.objects.get(id=hid)
        return JsonResponse(his.json())
    except History.DoesNotExist:
        return err("invalid hid")