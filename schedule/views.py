import datetime
import json
import os

from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from schedule.ScheduleService.neu import NEUSchedule
from schedule.models import NEUStudent

@csrf_exempt
def neu(request):
    if request.method == 'GET':
        return render(request, 'neu.html')
    elif request.method == 'POST':
        uid = request.POST['uid']
        password = request.POST['password']
        try:
            stu = NEUStudent.objects.get(uid=uid)
        except NEUStudent.DoesNotExist:
            stu = NEUStudent(uid=uid)
            stu.update_time = datetime.datetime.now()
        schedule = NEUSchedule()
        if schedule.update(uid=uid, password=password) is False:
            return HttpResponse("登录失败")
        base_dir = os.path.dirname(os.path.abspath(__name__))
        ics_dir = os.path.join(base_dir, 'media', 'ics', 'neu')
        filename = os.path.join(ics_dir, uid + '.ics')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(schedule.get_calendar().to_ical().decode())
        stu.name = schedule.name
        stu.save()
        r = schedule.get_json()
        r = {'schedule': r, 'url': 'http://fun.alphamj.cn/schedule/neu/' + uid}
        # js = json.dumps(r)
        return render(request, 'neu_table.html', r)
    else:
        return HttpResponse('?')

def neu_ics(request, uid):
    base_dir = os.path.dirname(os.path.abspath(__name__))
    ics_dir = os.path.join(base_dir, 'media', 'ics', 'neu')
    filename = os.path.join(ics_dir, uid + '.ics')
    try:
        with open(filename, encoding='utf-8') as f:
            return HttpResponse(f.read(), content_type='text/calendar; charset=UTF-8')
    except FileNotFoundError:
        return HttpResponseNotFound()
