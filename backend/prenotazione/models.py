from django.db import models
from django.db.models import F, Q, UniqueConstraint
from django.contrib.auth.models import User
from struttura.models import Struttura, Campo


class Prenotazione(models.Model):
    class Meta:
        # vincolo che permette di avere sempre fine > inizio
        # https://stackoverflow.com/questions/62610053/django-check-constraint-for-datetime
        constraints = [
            models.CheckConstraint(
                check=Q(fine__gt=F("inizio")), name="Controllo orari prenotazione"
            )
        ]

    prenotante = models.ForeignKey(to=User, on_delete=models.CASCADE)
    campo = models.ForeignKey(to=Campo, on_delete=models.CASCADE)
    inizio = models.DateTimeField()
    fine = models.DateTimeField()
