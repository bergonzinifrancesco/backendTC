from django.db import models
from enum import Enum

class CaratteristicheEnum(str, Enum):
    veloce = "veloce"
    agile = "agile"
    tecnico = "tecnico"
    fisico = "fisico"
    tattico = "tattico"
    acrobata = "acrobata"

class Caratteristiche(models.TextChoices):
    VELOCE = "veloce", ("Veloce")
    AGILE = "agile", ("Agile")
    TECNICO = "tecnico", ("Tecnico")
    FISICO = "fisico", ("Fisico")
    TATTICO = "tattico", ("Tattico")
    ACROBATA = "acrobata", ("Acrobata")

class PosizioniEnum(str, Enum):
    por = "POR"
    dif = "DIF"
    cen = "CEN"
    att = "ATT"
    ter = "DIF_TER"
    ala = "CEN_ALA"
    trq = "CEN_TRQ"
    qls = "QLS"
 
class Posizioni(models.TextChoices):
    PORTIERE = "POR", ("Portiere")
    DIFENSORE = "DIF", ("Difensore")
    CENTROCAMPISTA = "CEN", ("Centrocampista")
    ATTACCANTE = "ATT", ("Attaccante")
    TERZINO = "DIF_TER", ("Terzino")
    ALA = "CEN_ALA", ("Ala")
    TREQUARTISTA = "CEN_TRQ", ("Trequartista")
    QLS = "QLS", ("Qualsiasi")