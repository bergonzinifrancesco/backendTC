from ninja.router import Router
from ninja import ModelSchema
from ninja_jwt.authentication import JWTAuth
from struttura.models import AdminStruttura, Struttura, Campo, Recensione
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from typing import List

router = Router(tags=["Struttura"])


@router.get("/my_structures/", auth=JWTAuth(), response={200: List[int], 404: None})
def am_admin(request):
    """
    Restituisce l'id di tutte le strutture di cui l'utente attuale è admin.
    """
    try:
        tmp = AdminStruttura.objects.filter(admin=request.user)
        structures = [i["struttura_id"] for i in tmp.values()]

        # se la lista non è vuota
        if structures:
            return 200, structures
        return 404, None
    except ObjectDoesNotExist:
        return 404, None


class SchemaStruttura(ModelSchema):
    class Config:
        model = Struttura
        model_exclude = ["id"]


@router.get("/{id}/info/", response={200: SchemaStruttura, 404: str})
def get_structure_info(request, id: int):
    try:
        tmp = Struttura.objects.get(id=id)
        return 200, tmp
    except ObjectDoesNotExist:
        return 404, "La struttura selezionata non esiste."


@router.get("/list_structures/", response={200: List[int], 404: str})
def list_structures(request):
    """
    Restituisce tutti gli id delle strutture presenti.
    """
    try:
        tmp = Struttura.objects.all()
        return 200, [e.id for e in tmp]
    except ObjectDoesNotExist:
        return 404, "Non ci sono strutture memorizzate."


class CampoSchema(ModelSchema):
    class Config:
        model = Campo
        model_exclude = ["struttura", "id"]


@router.get(
    "/{id_struttura}/info_campi/", response={200: List[CampoSchema], 404: str, 500: str}
)
def get_info_campi(request, id_struttura: int):
    """
    Restituisce info sui campi appartenenti alla struttura.<br/>
    Dà errore se la struttura non ha campi.
    """
    try:
        struttura = Struttura.objects.get(id=id_struttura)
        tmp = Campo.objects.filter(struttura=struttura)
        if tmp:
            return 200, tmp
        return 404, "Non ci sono campi per questa struttura."
    except Exception as e:
        return 500, str(e)


@router.get("/{id_struttura}/voto_medio/", response={200: float, 404: str, 500: str})
def get_voto_medio(request, id_struttura: int):
    """
    Restituisce il voto medio associato alla struttura.<br/>
    Segnala errore se non ci sono recensioni.
    """
    try:
        struttura = Struttura.objects.get(id=id_struttura)
        media_voti = Recensione.objects.filter(struttura=struttura).aggregate(
            Avg("voto")
        )["voto__avg"]
        if media_voti:
            return 200, round(media_voti * 2) / 2
        return 404, "Non ci sono voti per questa struttura."
    except Exception as e:
        return 500, str(e)


class RecensioneSchema(ModelSchema):
    class Config:
        model = Recensione
        model_exclude = ["id", "votante", "struttura"]


@router.put(
    "/{id_struttura}/recensione/",
    response={204: None, 404: str, 500: str},
    auth=JWTAuth(),
)
def put_voto(request, id_struttura: int, update_recensione: RecensioneSchema):
    try:
        try:
            struttura = Struttura.objects.get(id=id_struttura)
        except Exception as e:
            return 404, str(e)

        recensione, created = Recensione.objects.update_or_create(
            votante=request.user,
            struttura=struttura,
            defaults={
                "voto": update_recensione.voto,
                "descrizione": update_recensione.descrizione,
            },
        )
        print(recensione, created)
        return 204, None
    except Exception as e:
        return 500, str(e)
