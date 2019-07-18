from django.db import models


class Dialog(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=False)
    text = models.TextField()

    def __str__(self):
        return "{}:".format(self.id) + self.text[:10] + "...." if len(self.text) > 10 else self.text


class RegisteredUser(models.Model):
    name = models.TextField()
    start = models.IntegerField()
    end = models.IntegerField()
    index = models.IntegerField()

    def __str__(self):
        return self.name


class Label(models.Model):
    text = models.ForeignKey(Dialog, on_delete=models.PROTECT)
    label = models.IntegerField()
    user = models.ForeignKey(RegisteredUser, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.name + ":" + str(self.label)
