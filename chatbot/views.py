from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        history = request.user.chat_history.all()
    else:
        history = []
    print(request.META)
    return render(request, 'chatbot/index.html', {'current_user': request.user, 'history': history})


def login(request):
    return render(request, 'chatbot/login.html')


@login_required(login_url='/login')
def user_center(request):
    return render(request, 'chatbot/user_center.html', {'current_user': request.user})
