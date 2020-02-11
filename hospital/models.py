import uuid as uuid
from datetime import datetime, timedelta

from django.db import models

# Create your models here.
# 患者表
# 主键id，uuid，患者编号，患者姓名，年龄，患病信息，微信号，患者状态，所在地区，图片
#
# 医生表
# 主键id，uuid，医生编号，医生姓名，性别，微信号，医生级别，积分
#
# 消息表
# 主键id，uuid，消息发送时间，发送人，接受人，消息信息
#
# 病史表
# 主键id，uuid，患者编号，患者情况，诊断建议，诊断医生，诊断时间


class User(models.Model):
    openid = models.CharField(primary_key=True, max_length=32)
    role = models.IntegerField(default=0)  # 1 是医生，2是患者


class Doctor(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4)
    did = models.CharField(max_length=64, unique=True, db_index=True)
    name = models.TextField(null=True, blank=True)
    gender = models.IntegerField(default=0)  # 1: male, 2: female
    rank = models.IntegerField(default=1)
    credits = models.IntegerField(default=0)
    wechat = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.TextField(default="code")
    token = models.TextField(null=True, blank=True)

    def json(self):
        d = {
            'id': self.id,
            'uuid': self.uuid,
            'did': self.did,
            'name': self.name,
            'gender': self.gender,
            'rank': self.rank,
            'credits': self.credits
        }
        return d


class Patient(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4)
    pid = models.CharField(max_length=64, unique=True, db_index=True)
    name = models.TextField()
    age = models.IntegerField()
    gender = models.IntegerField()  # 1: male, 2: female
    wechat = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    location = models.TextField()
    phone = models.TextField(blank=True, null=True)

    def json(self):
        d = {
            'id': self.id,
            'uuid': self.uuid,
            'pid': self.pid,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'location': self.location,
            'phone': self.phone
        }
        return d


class Pictures(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    pic = models.ImageField()


class Message(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4)
    time = models.DateTimeField()
    sender = models.TextField(db_index=True)
    receiver = models.TextField(db_index=True)
    message = models.TextField()


class History(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
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
        return d


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
    time = models.DateTimeField(auto_now=True)