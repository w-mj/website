from django.db import models

# Create your models here.


class NEUStudent(models.Model):
    uid = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=10)
    update_time = models.DateTimeField(auto_now=True)