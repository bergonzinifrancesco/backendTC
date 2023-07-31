from django.db import models

# Create your models here.
class Struttura(models.Model):
    # l'id chiave primaria è generato automaticamente da django
    nome = models.CharField(max_length=150)
    fondazione = models.DateField(null=True)
    # lat e long verranno inseriti assieme tramite API
    lat = models.FloatField(
        null=True,
    )
    long = models.FloatField(
        null=True
    )
    dimensione = models.DecimalField(
        null=True,
        max_digits=5,
        decimal_places=2
    )
    spogliatoi = models.BooleanField(
        default=False
    )

