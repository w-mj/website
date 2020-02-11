from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('openid', 'role',)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('did', 'name', 'gender', 'rank', 'credits')

class PatientAdmin(admin.ModelAdmin):
    list_display = ('pid', 'name', 'age', 'gender', 'location')

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'ill', 'info', 'doctor', 'diag_time', 'send_time', 'rank')

class AcceptAdmin(admin.ModelAdmin):
    list_display = ('history', 'doctor', 'finish')

class RankUpHistoryAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'history', 'time')


admin.site.register(User, UserAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Pictures)
admin.site.register(Message)
admin.site.register(History, HistoryAdmin)
admin.site.register(PictureTable)
admin.site.register(Accept, AcceptAdmin)
admin.site.register(RankUPHistory, RankUpHistoryAdmin)


# Register your models here.
