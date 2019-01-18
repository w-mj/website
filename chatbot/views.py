from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        history = request.user.chat_history.all()
    else:
        history = []
    return render(request, 'index.html', {'current_user': request.user, 'history': history})


def login(request):
    return render(request, 'login.html')


def user_center(request):
    return render(request, 'user_center.html', {'current_user': request.user})
