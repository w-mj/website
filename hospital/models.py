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
    id = models.IntegerField(primary_key=True, auto_created=True)
    uuid = models.UUIDField()
    did = models.TextField(unique=True, db_index=True)
    name = models.TextField()
    gender = models.IntegerField(default=0)  # 1: male, 2: female
    rank = models.IntegerField(default=1)
    credits = models.IntegerField(default=0)
    wechat = models.ForeignKey(User, on_delete='SET_NULL')

    def info(self):
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
    id = models.IntegerField(primary_key=True, auto_created=True)
    uuid = models.UUIDField()
    pid = models.TextField(unique=True, db_index=True)
    name = models.TextField()
    age = models.IntegerField()
    gender = models.IntegerField()  # 1: male, 2: female
    wechat = models.ForeignKey(User, on_delete='SET_NULL')
    location = models.TextField()
    phone = models.TextField(blank=True, null=True)

    def info(self):
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
    id = models.IntegerField(primary_key=True, auto_created=True)
    uuid = models.UUIDField()
    time = models.DateTimeField()
    sender = models.TextField(db_index=True)
    receiver = models.TextField(db_index=True)
    message = models.TextField()


class History(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    patient = models.ForeignKey(Patient, on_delete='SET_NULL')
    ill = models.TextField()
    state = models.TextField()
    doctor = models.ForeignKey(to=Doctor, on_delete='SET_NULL', null=True)
    diag_time = models.DateTimeField()
    send_time = models.DateTimeField()
    rank = models.IntegerField()

    def info(self):
        d = {
            'id': self.id,
            'ill': self.ill,
            'state': self.state,
            'doctor': self.doctor.info(),
            'patient': self.patient.info(),
            'send_time': str(self.send_time.time()),
            'diag_time': str(self.diag_time.time()),
            'rank': self.rank
        }
        return d


class PictureTable(models.Model):
    pic = models.ForeignKey(Pictures, on_delete='SET_NULL')
    patient = models.ForeignKey(History, on_delete='SET_NULL')
