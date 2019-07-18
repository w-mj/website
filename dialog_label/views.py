from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET

from dialog_label import models


@require_GET
def console(request):
    users = models.RegisteredUser.objects.all()
    data = {u: u.index - u.start for u in users}
    count = models.Dialog.objects.count()
    return render(request, 'dialog_label/console.html', {'users': data, 'count': count})


def get_dialog(request):
    uname = request.GET.get('uid', None)
    if uname is None or models.RegisteredUser.objects.filter(id=uname).count() == 0:
        return render(request, 'dialog_label/index.html', {'user': None})
    user = models.RegisteredUser.objects.get(id=uname)
    index = user.index
    dialog = models.Dialog.objects.get(id=index)
    return JsonResponse({'did': dialog.id, 'text': dialog.text.split('__eou__')})


def index(request):
    uname = request.GET.get('uname', None)
    if uname is None or models.RegisteredUser.objects.filter(name=uname).count() == 0:
        return render(request, 'dialog_label/index.html', {'login': False})
    else:
        return render(request, 'dialog_label/index.html',
                      {'login': True,
                       'user': models.RegisteredUser.objects.get(name=uname),
                       'count': models.Dialog.objects.count()
                       })


def label(request):
    ls = request.POST['label']
    uid = request.POST['uid']
    did = request.POST['did']
    if not ls or not uid or not did:
        return JsonResponse({'result': 'error'})
    label_value = 0
    ls = reversed(ls)
    # print(ls)

    for c in ls:
        label_value = (label_value << 3) + int(c)
    user = models.RegisteredUser.objects.get(id=uid)

    label_item = models.Label()
    label_item.label = label_value
    label_item.text = models.Dialog.objects.get(id=did)
    label_item.user = user
    label_item.save()
    index = int(did) + 1
    user.index = index
    user.save()
    dialog = models.Dialog.objects.get(id=index)
    return JsonResponse({'did': dialog.id, 'text': dialog.text.split('__eou__')})


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


def download(request):
    uid = request.GET.get('uid', None)
    if uid is None:
        return HttpResponse("no content")
    try:
        user = models.RegisteredUser.objects.get(id=uid)
    except models.RegisteredUser.DoesNotExist:
        return HttpResponse("no content")
    response = ""
    labels = models.Label.objects.filter(user=user)
    for label in labels:
        label_v = []
        t = label.label
        while t > 0:
            label_v.append(t & 7)
            t = t >> 3
        label_s = [sent_dict[x] for x in label_v]
        response += "{}:".format(label.text.id) + "".join(label_s) + "\n"
    return HttpResponse(response)
