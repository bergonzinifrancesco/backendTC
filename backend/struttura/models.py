from django.db import models
from django.contrib.auth.models import User

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


class Campo(models.Model):
    # necessaria per creare la chiave composta
    class Meta:
        unique_together = (('struttura', 'num_campo'),)
    
    struttura = models.OneToOneField(to=Struttura, on_delete=models.CASCADE, primary_key=True, db_column="struttura")
    num_campo = models.PositiveSmallIntegerField()
    costo_orario = models.DecimalField(max_digits=3, decimal_places=1)
    coperto = models.BooleanField(null=True)
    illuminato = models.BooleanField(null=True)

    class TipiCampo(models.TextChoices):
      SINTETICO = "sintetico", ("sintetico")
      NATURALE = "naturale", ("naturale")
      PARQUET = "parquet", ("parquet")
      CEMENTO = "cemento", ("cemento")
      PALESTRA = "palestra", ("palestra")
    
    tipo_superficie = models.CharField(
        choices=TipiCampo.choices,
        null=True,
        max_length=9
    )


class AdminStruttura(models.Model):
    struttura = models.ForeignKey(to=Struttura, on_delete=models.CASCADE)
    admin = models.ForeignKey(to=User, on_delete=models.CASCADE)