from ninja.router import Router
from ninja import ModelSchema
from ninja_jwt.authentication import JWTAuth
from struttura.models import Struttura, Campo, AdminStruttura
from prenotazione.models import Prenotazione
from django.core.exceptions import ObjectDoesNotExist
from typing import List
from django.db.models.functions import Now
from django.contrib.auth.models import User

import datetime

router = Router(tags=["Prenotazione"])


class BookingSchema(ModelSchema):
    class Config:
        model = Prenotazione
        model_exclude = ["id"]


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


@router.post(
    "/modifica_calendario/{id_struttura}/",
    response={204: None, 403: str, 404: str, 500: str},
    auth=JWTAuth(),
)
def modifica_calendario(request, id_struttura: int, bookings: List[BookingSchema]):
    try:
        try:
            struttura = Struttura.objects.get(id=id_struttura)
        except ObjectDoesNotExist:
            return 404, "Struttura non trovata."
        except Exception as e:
            raise e
        try:
            AdminStruttura.objects.get(struttura=struttura, admin=request.user)
        except ObjectDoesNotExist:
            return 403, "Non sei admin della struttura."
        except Exception as e:
            raise e

        # Cancellazione del calendario (vedi frontend)
        campi = Campo.objects.filter(struttura=struttura)
        to_be_deleted = Prenotazione.objects.filter(campo__in=campi, inizio__gte=Now())
        print("to_be_deleted", to_be_deleted)
        to_be_deleted.delete()

        # Filtraggio degli eventi presentati
        now = datetime.datetime.now(datetime.timezone.utc)
        valid_bookings = [
            b for b in bookings if ((b.fine > b.inizio) and (b.inizio >= now))
        ]

        # Inserimento degli eventi nel db (uno alla volta)
        for booking in valid_bookings:
            try:
                prenotante = User.objects.get(id=booking.prenotante)
                campo = Campo.objects.get(id=booking.campo)
                Prenotazione.objects.create(
                    prenotante=prenotante,
                    campo=campo,
                    inizio=booking.inizio,
                    fine=booking.fine,
                )
            except Exception as e:
                print(e)

        return 204, None
    except Exception as e:
        return 500, str(e)
