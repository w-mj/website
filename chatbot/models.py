from django.db import models
from django.contrib.auth.models import User


class ChatHistory(models.Model):
    user = models.ForeignKey(User, related_name='chat_history', on_delete=models.CASCADE)
    is_response = models.BooleanField()
    text = models.TextField()
    time = models.DateTimeField(auto_now=True)
