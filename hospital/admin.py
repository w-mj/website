from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('openid', 'role', 'name', 'gender', 'age', 'location', 'phone')

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('did', 'wechat', 'credits', 'rank', 'code')


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'ill', 'info', 'doctor', 'diag_time', 'send_time', 'rank')

class AcceptAdmin(admin.ModelAdmin):
    list_display = ('history', 'doctor', 'finish')

class RankUpHistoryAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'history', 'time', 'inc')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'history', 'sender', 'time', 'text')


admin.site.register(User, UserAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Pictures)
admin.site.register(Message, MessageAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(PictureTable)
admin.site.register(Accept, AcceptAdmin)
admin.site.register(RankUPHistory, RankUpHistoryAdmin)


# Register your models here.
