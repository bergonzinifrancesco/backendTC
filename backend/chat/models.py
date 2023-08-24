from django.db import models
from django.contrib.auth import get_user_model
from struttura.models import Struttura

toUser = get_user_model()


class Message(models.Model):
    message = models.CharField(max_length=500)
    user = models.ForeignKey(to=toUser, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    struttura = models.ForeignKey(
        to=Struttura, on_delete=models.CASCADE, blank=True, null=True
    )
