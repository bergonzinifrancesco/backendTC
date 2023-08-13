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
    long = models.FloatField(null=True)
    dimensione = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    spogliatoi = models.BooleanField(default=False)


class Campo(models.Model):
    class Meta:
        unique_together = (("struttura", "num_campo"),)

    id = models.BigAutoField(primary_key=True, auto_created=True)
    struttura = models.ForeignKey(
        to=Struttura, on_delete=models.CASCADE, db_column="struttura"
    )
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
        choices=TipiCampo.choices, null=True, max_length=9
    )


class AdminStruttura(models.Model):
    struttura = models.ForeignKey(to=Struttura, on_delete=models.CASCADE)
    admin = models.ForeignKey(to=User, on_delete=models.CASCADE)


class Recensione(models.Model):
    class Meta:
        unique_together = (("votante", "struttura"),)

    class Voti(models.IntegerChoices):
        UNO = 1
        DUE = 2
        TRE = 3
        QUATTRO = 4
        CINQUE = 5

    votante = models.ForeignKey(to=User, on_delete=models.CASCADE)
    struttura = models.ForeignKey(to=Struttura, on_delete=models.CASCADE)
    voto = models.IntegerField(choices=Voti.choices, null=False)
    descrizione = models.CharField(max_length=200, null=True)
