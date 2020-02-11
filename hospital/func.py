from time import time

from django.http import HttpResponseNotFound, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .form import photoForm
from .models import *

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
            return JsonResponse({'error': "upload image fail."})
    elif request.method == 'GET':
        if not request.GET.get('img'):
            return render(request, "hospital/index.html")
        try:
            img = Pictures.objects.get(id=request.GET.get('img', None))
        except Pictures.DoesNotExist:
            return HttpResponseNotFound()
        return HttpResponse(img.pic, content_type='image/png')
