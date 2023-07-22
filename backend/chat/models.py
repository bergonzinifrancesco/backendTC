from django.db import models
from django.contrib.auth import get_user_model


toUser = get_user_model()

class Message(models.Model):
    message = models.JSONField()
    user = models.ForeignKey(to=toUser, on_delete=models.CASCADE, null=True, blank=True)