from ninja.router import Router
from ninja import ModelSchema
from ninja_jwt.authentication import JWTAuth
from struttura.models import Struttura, Campo
from prenotazione.models import Prenotazione
from django.core.exceptions import ObjectDoesNotExist
from typing import List

router = Router(tags=["Prenotazione"])


class BookingSchema(ModelSchema):
    class Config:
        model = Prenotazione
        model_exclude = ["prenotante"]


@router.get("/get_bookings/", response={200: List[BookingSchema], 404: str})
def get_bookings_for_field(request, structure_id: int, field_id: int = None):
    """
    Restituisce tutte le prenotazioni effettuate per la struttura ed il campo indicati.
    """
    try:
        struttura = Struttura.objects.get(id=structure_id)
    except ObjectDoesNotExist:
        return 404, "Nessuna struttura con l'id indicato"

    try:
        elenco_campi = Campo.objects.filter(struttura=struttura)
    except ObjectDoesNotExist:
        return 404, "Non ci sono campi associati alla struttura"

    if field_id:
        try:
            campo = elenco_campi.get(num_campo=field_id)
        except Exception as e:
            return 404, str(e)

        result = Prenotazione.objects.filter(campo=campo)
    else:
        result = []
        for c in elenco_campi:
            result += Prenotazione.objects.filter(campo=c)

    if not result:
        return 404, "Non ci sono prenotazioni per la struttura indicata."

    return 200, result


class AddBookingSchema(ModelSchema):
    class Config:
        model = Prenotazione
        model_exclude = ["prenotante", "id"]

    struttura: int


@router.post("/create_booking/", response={200: str, 400: str}, auth=JWTAuth())
def add_booking(request, booking: AddBookingSchema):
    try:
        tmp = booking.dict()

        struttura = Struttura.objects.get(id=tmp["struttura"])
        campo = Campo.objects.get(num_campo=tmp["campo"], struttura=struttura)

        Prenotazione.objects.create(
            prenotante=request.user, campo=campo, inizio=tmp["inizio"], fine=tmp["fine"]
        ).save()

        return 200, "Prenotazione salvata con successo"
    except Exception as e:
        return 400, str(e)
