import os

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class ChatHistory(models.Model):
    user = models.ForeignKey(User, related_name='chat_history', on_delete=models.CASCADE)
    is_response = models.BooleanField()
    text = models.TextField()
    emotion = models.FloatField(default=-1)
    time = models.DateTimeField(auto_now=True)


class Avatar(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatar/default.png', upload_to='avatar')


@receiver(models.signals.pre_save, sender=Avatar)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is changed.
    """
    if not instance:
        return False
    try:
        old_file = Avatar.objects.get(user=instance.user).avatar
    except Avatar.DoesNotExist:
        return False

    new_file = instance.avatar
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
