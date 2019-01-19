"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import chatbot.views
import chatbot.auth
import chatbot.func
from website import settings
from .deploy import deploy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', chatbot.views.index),
    path('login', chatbot.views.login),
    path('user', chatbot.views.user_center),
    path('signup', chatbot.auth.signup),
    path('signin', chatbot.auth.signin),
    path('logout', chatbot.auth.logout),
    path('changepsw', chatbot.auth.changePsw),
    path('uploadavatar', chatbot.auth.changeAvatar),

    path('chat', chatbot.func.chat),
    path('separation', chatbot.func.separation),
    path('deploy', deploy)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
