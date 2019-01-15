from django.shortcuts import render
from .models import ChatHistory
from django.contrib.auth.models import User


def index(request):
    if request.user.is_authenticated:
        history = request.user.chat_history.all()
    else:
        history = []
    return render(request, 'index.html', {'current_user': request.user, 'history': history})


def login(request):
    return render(request, 'login.html')
