from django.shortcuts import render


def chatbot_index(request):
    return render(request, 'index.html')
