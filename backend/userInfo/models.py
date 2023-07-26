from django.db import models
from django.contrib.auth.models import User
from backend.settings import MEDIA_ROOT
from django_countries.fields import CountryField
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField
from userInfo.choices import Posizioni, Caratteristiche


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
        max_length=20
    )
    bio = models.CharField(
        max_length=300,
        blank=True
    )

class AvatarUtente(models.Model):
    def uploadTo(instance, filename):
        return f"{instance.img_id}/{filename}"

    img_id = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True, unique=True)
    image = models.ImageField(upload_to=uploadTo)

class PosizioniGioco(models.Model):
    pos_id = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True, unique=True)
    
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
