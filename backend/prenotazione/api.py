from ninja.router import Router
from ninja import ModelSchema
from ninja_jwt.authentication import JWTAuth
from struttura.models import Struttura, Campo
from prenotazione.models import Prenotazione
from django.core.exceptions import ObjectDoesNotExist
from typing import List

router = Router(tags=['Prenotazione'])


class BookingSchema(ModelSchema):
  class Config:
    model = Prenotazione
    model_fields = "__all__"


@router.get('/get_bookings/', response={200: List[BookingSchema], 404: str})
def get_bookings_for_field(request, structure_id: int, field_id: int = None):
  '''
  Restituisce tutte le prenotazioni effettuate per la struttura ed il campo indicati.
  '''
  try:
    struttura = Struttura.objects.get(id=structure_id)
  except ObjectDoesNotExist:
    return 404, "Nessuna struttura con l'id indicato"
  
  if field_id:
    tmp = Prenotazione.objects.filter(struttura=struttura, num_campo=field_id)
  else:
    tmp = Prenotazione.objects.filter(struttura=struttura)

  if not tmp:
    return 404, "Non ci sono prenotazioni per la struttura indicata."
  
  return 200, tmp


class AddBookingSchema(ModelSchema):
  class Config:
    model = Prenotazione
    model_exclude = ["prenotante", "id"]
  struttura: int

@router.post("/create_booking/", response={200: str, 400: str}, auth=JWTAuth())
def add_booking(request, booking: AddBookingSchema):
  try:
    tmp = booking.dict()
    
    struttura = Struttura.objects.get(id=tmp['struttura'])
    campo = Campo.objects.get(num_campo=tmp['campo'], struttura=struttura)

    Prenotazione.objects.create(
      prenotante=request.user,
      campo=campo,
      inizio=tmp['inizio'],
      fine=tmp['fine']
    ).save()

    return 200, "Prenotazione salvata con successo"
  except Exception as e:
    return 400, str(e)