from django.db import models
from django.contrib.auth.models import User
from backend.settings import MEDIA_ROOT
from django_countries.fields import CountryField
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField

class InfoAvanzate(models.Model):
    user_id = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True, unique=True)

    peso = models.DecimalField(
        blank=True,
        decimal_places=1,
        max_digits=4
    )
    altezza = models.PositiveSmallIntegerField(
        blank=True
    )
    avatar = models.ImageField(
        upload_to="{int:id}/avatar",
        max_length=1000,
        blank=True
    )
    data_nascita = models.DateField(
        blank=True,
        default=date(1900,1,1)
    )
    nazionalità = CountryField(
        default="IT"
    )
    numero_telefono = PhoneNumberField(
        blank=True,
        region="IT",
        max_length=12
    )
    bio = models.CharField(
        max_length=300,
        blank=True
    )


class PosizioniGioco(models.Model):
    pos_id = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True, unique=True)
    
    class Posizioni(models.TextChoices):
        PORTIERE = "POR", ("Portiere")
        DIFENSORE = "DIF", ("Difensore")
        CENTROCAMPISTA = "CEN", ("Centrocampista")
        ATTACCANTE = "ATT", ("Attaccante")
        TERZINO = "DIF_TER", ("Terzino")
        ALA = "CEN_ALA", ("Ala")
        TREQUARTISTA = "CEN_TRQ", ("Trequartista")
        QLS = "QLS", ("Qualsiasi")
    
    preferita = models.CharField(
        max_length=7,
        choices=Posizioni.choices,
        default=Posizioni.QLS
    )
    alternativa = models.CharField(
        max_length=7,
        choices=Posizioni.choices,
        default=Posizioni.QLS,
        blank=True
    )
    alternativa2 = models.CharField(
        max_length=7,
        choices=Posizioni.choices,
        default=Posizioni.QLS,
        blank=True
    )


class CaratteristicheGioco(models.Model):
    car_id = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True, unique=True)
    
    class Caratteristiche(models.TextChoices):
        VELOCE = "veloce", ("Veloce")
        AGILE = "agile", ("Agile")
        TECNICO = "tecnico", ("Tecnico")
        FISICO = "fisico", ("Fisico")
        TATTICO = "tattico", ("Tattico")
        ACROBATA = "acrobata", ("Acrobata")
    
    principale = models.CharField(
        choices=Caratteristiche.choices,
        max_length=8,
    )
    secondaria = models.CharField(
        choices=Caratteristiche.choices,
        max_length=8,
        blank=True
    )
    terziaria = models.CharField(
        choices=Caratteristiche.choices,
        max_length=8,
        blank=True
    )
