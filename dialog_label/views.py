import os

from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET

from dialog_label import models


@require_GET
def console(request):
    users = models.RegisteredUser.objects.all()
    data = {u: u.index - u.start for u in users}
    count = models.Dialog.objects.count()
    deleted = models.Dialog.objects.filter(is_deleted=True).count()
    return render(request, 'dialog_label/console.html', {'users': data, 'count': count, 'deleted_count': deleted})


def return_dialog(user):
    if user.rank < 5:
        # 普通用户
        index = index0 = user.index
        if index == user.end:
            return JsonResponse({'did': -1, 'text': ["没有更多对话了"]})

        dialog = models.Dialog.objects.get(id=index)
        while dialog.is_deleted:
            index += 1
            dialog = models.Dialog.objects.get(id=index)
        if index != index0:
            user.index = index
            user.save()
        return JsonResponse({'did': dialog.id, 'text': dialog.text.split('__eou__')})
    else:
        qs = models.Label.objects.all()
        labels = qs.values_list('text_id', flat=True).distinct()
        for text_id in labels:
            dialog = models.Dialog.objects.get(id=text_id)
            if dialog.is_deleted:
                continue
            label_in = qs.filter(text_id=text_id)
            if label_in.count() >= 2:
                same = True
                for i in range(len(label_in)):
                    # print(label_in[i].label, end=' ')
                    if label_in[i].user == user:
                        same = True
                        break
                    if i < len(label_in) - 1 and label_in[i].label != label_in[i + 1].label:
                        same = False

                # print()
                if not same:
                    dialog = label_in[0].text
                    return JsonResponse({'did': dialog.id, 'text': dialog.text.split('__eou__'),
                                         'userchoice': [x.dict(True) for x in label_in]})
        # 高级用户
        # labels = models.Label.objects.
        return JsonResponse({'did': -1, 'text': ["没有更多对话了"]})


def get_dialog(request):
    uname = request.GET.get('uid', None)
    if uname is None or models.RegisteredUser.objects.filter(id=uname).count() == 0:
        return render(request, 'dialog_label/index.html', {'user': None})
    user = models.RegisteredUser.objects.get(id=uname)
    return return_dialog(user)


def index(request):
    uname = request.GET.get('uname', None)
    if uname is None or models.RegisteredUser.objects.filter(name=uname).count() == 0:
        return render(request, 'dialog_label/index.html', {'login': False})
    else:
        user = models.RegisteredUser.objects.get(name=uname)
        return render(request, 'dialog_label/index.html',
                      {'login': True,
                       'user': user.json()
                       })


def label(request):
    ls = request.POST['label']
    uid = request.POST['uid']
    did = request.POST['did']
    os.system("echo {}:{}:{} >> ../backup/backup.txt".format(uid, did, ls))
    if not ls or not uid or not did:
        return JsonResponse({'result': 'error'})

    user = models.RegisteredUser.objects.get(id=uid)

    try:
        label1 = models.Label.objects.get(user=user, text_id=did)
        label1.label = ls
        label1.save()
    except models.Label.DoesNotExist:
        label_item = models.Label()
        label_item.label = int(str(ls))
        label_item.text = models.Dialog.objects.get(id=did)
        label_item.user = user
        label_item.save()
    index = int(did) + 1
    user.index = index
    user.save()
    return return_dialog(user)


def clear(request):
    models.Dialog.objects.all().delete()
    return HttpResponse("OK")


@require_POST
def upload(request):
    file = request.FILES['dialog']
    cnt = 0
    for line in file:
        d = models.Dialog()
        d.id = cnt
        d.text = line.decode()
        d.save()
        cnt += 1
    return HttpResponse(str(models.Dialog.objects.count()))


sent_dict = ['ER', '乐', '好', '哀', '惧', '恶', '无']


def download_deleted(request):
    deleted = models.Dialog.objects.all()
    res = {k.id: 1 if k.is_deleted else 0 for k in deleted}
    return JsonResponse(res)


def download(request):
    uid = request.GET.get('uid', None)
    if uid is None:
        return HttpResponse("no content")
    try:
        if uid == "deleted":
            return download_deleted(request)
        user = models.RegisteredUser.objects.get(id=uid)
    except models.RegisteredUser.DoesNotExist:
        return HttpResponse("no content")
    labels = models.Label.objects.filter(user=user)
    labels = [x.dict() for x in labels]
    return JsonResponse({'user': uid, 'labels': labels})


def delete(request):
    uid = request.POST['uid']
    did = request.POST['did']
    print("delete", uid, did)
    try:
        user = models.RegisteredUser.objects.get(id=uid)
        if user.rank < 5:
            return JsonResponse({"result": "fail1"})
        dialog = models.Dialog.objects.get(id=did)
        dialog.is_deleted = True
        dialog.save()
        return JsonResponse({"result": "ok"})
    except models.RegisteredUser.DoesNotExist:
        return JsonResponse({"result": "fail"})

