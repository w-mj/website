import json

from django.db import models


class Dialog(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=False)
    text = models.TextField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "{}:".format(self.id) + self.text[:10] + "...." if len(self.text) > 10 else self.text


class RegisteredUser(models.Model):
    name = models.TextField()
    start = models.IntegerField()
    end = models.IntegerField()
    index = models.IntegerField()
    rank = models.IntegerField()

    def __str__(self):
        return self.name

    def json(self):
        return json.dumps({k: v for k, v in self.__dict__.items() if k[0] != '_'})


class Label(models.Model):
    text = models.ForeignKey(Dialog, on_delete=models.PROTECT)
    label = models.IntegerField()
    user = models.ForeignKey(RegisteredUser, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.name + ":" + str(self.label)

    def dict(self, user=False):
        if user:
            return {self.user.name: self.label}
        return {self.text_id: self.label}
