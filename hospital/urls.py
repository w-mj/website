from django.urls import path

from hospital import views, func

urlpatterns = [
    path('index', views.index),
    path('picture', func.picture),
    path('ill', func.uploadill),
    path('checkcode', func.checkcode),
    path('doctorsignup', func.doctor_signup),
    path('getpatients', func.get_patients),
    path('startdiagnosis', func.start_diagnosis),
    path('finishdiagnosis', func.finish_diagnosis),
    path('rankuphistory', func.rank_up_history),
    path('history', func.history),
    path('adddoctor', func.add_doctor),
    path('statistic', func.statistic)
]