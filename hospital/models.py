import uuid as uuid
from datetime import datetime, timedelta

from django.db import models


class User(models.Model):
    openid = models.CharField(primary_key=True, max_length=32)
    role = models.IntegerField(default=2)  # 1 是医生，2是患者
    name = models.TextField(default="未填写")
    gender = models.IntegerField(default=0)  # 1: male, 2: female
    age = models.IntegerField(default=0)
    location = models.TextField(default="未填写")
    phone = models.TextField(default="未填写")

    def json(self):
        d = {
            'openid': self.openid,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'location': self.location,
            'phone': self.phone,
            'role': self.role
        }
        return d

    def __str__(self):
        return str(self.name) + ("[医生]" if self.role == 1 else "[患者]") + self.openid


class Doctor(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4)
    did = models.CharField(max_length=64, unique=True, db_index=True)
    rank = models.IntegerField(default=1)
    credits = models.IntegerField(default=0)
    wechat = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.TextField(default="code")
    token = models.TextField(null=True, blank=True)

    def json(self):
        d = {
            'did': self.did,
            'rank': self.rank,
            'credits': self.credits
        }
        d.update(self.wechat.json())
        return d

    def __str__(self):
        return str(self.id) + " " + str("del" if self.wechat is None else self.wechat.name)


class Pictures(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    pic = models.ImageField()


class History(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ill = models.TextField()
    info = models.TextField()
    doctor = models.ForeignKey(to=Doctor, on_delete=models.SET_NULL, null=True)
    diag_time = models.DateTimeField(null=True)
    send_time = models.DateTimeField()
    rank = models.IntegerField()

    def json(self):
        st = self.send_time
        st += timedelta(hours=+8)
        dt = self.diag_time
        if dt is not None:
            dt += timedelta(hours=+8)
        d = {
            'id': self.id,
            'ill': self.ill,
            'info': self.info,
            'doctor': None if self.doctor is None else self.doctor.json(),
            'patient': self.patient.json(),
            'send_time': st.strftime("%Y-%m-%d %H:%M:%S"),
            'diag_time': None if self.diag_time is None else dt.strftime("%Y-%m-%d %H:%M:%S"),
            'rank': self.rank
        }
        pics = PictureTable.objects.filter(history=self)
        pics = [x.pic.id for x in pics]
        d.update({"pics": pics})
        if self.doctor is not None:
            d.update({"state": Accept.objects.get(history=self, doctor=self.doctor).finish})
        return d

    def __str__(self):
        return "{} {}: {}".format(self.id, self.patient.name, self.ill)


class PictureTable(models.Model):
    pic = models.ForeignKey(Pictures, on_delete=models.SET_NULL, null=True)
    history = models.ForeignKey(History, on_delete=models.SET_NULL, null=True)


class Accept(models.Model):
    # 接诊表
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    history = models.ForeignKey(History, on_delete=models.SET_NULL, null=True)
    finish = models.BooleanField()


class RankUPHistory(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    history = models.ForeignKey(History, on_delete=models.SET_NULL, null=True)
    inc = models.IntegerField()
    time = models.DateTimeField(auto_now=True)


class Message(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    time = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    history = models.ForeignKey(History, on_delete=models.SET_NULL, null=True)
    text = models.TextField()

    def json(self):
        st = self.time
        st += timedelta(hours=+8)
        d = {
            'id': self.id,
            'time': st.strftime("%Y-%m-%d %H:%M:%S"),
            'sender': self.sender.json(),
            'history': self.history.id,
            'text': self.text
        }
        return d
