from ninja.router import Router
from ninja import ModelSchema, Schema
from ninja_jwt.authentication import JWTAuth
from struttura.models import AdminStruttura, Struttura, Campo, Recensione
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Q
from typing import List, Optional, Tuple
from enum import Enum, IntEnum
from pydantic import BaseModel, ValidationError
import math

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


class ModifyStrutturaSchema(ModelSchema):
    class Config:
        model = Struttura
        model_exclude = ["id", "lat", "long"]
        model_fields_optional = "__all__"


@router.patch(
    "/{id_struttura}/modify_info/",
    response={204: None, 403: str, 404: str, 500: str},
    auth=JWTAuth(),
)
def modify_structure_info(request, id_struttura: int, new_info: ModifyStrutturaSchema):
    """
    Tutti i campi del dizionario JSON sono opzionali.
    """
    try:
        try:
            struttura = Struttura.objects.get(id=id_struttura)
        except:
            return 404, "Struttura non trovata"
        try:
            admin = AdminStruttura.objects.get(struttura=struttura, admin=request.user)
        except Exception as e:
            return 403, "Non sei admin di questa struttura."

        struttura.__dict__.update(new_info.__dict__)
        struttura.save()
        return 204, None
    except Exception as e:
        return 500, str(e)


class FilterOptions(Schema):
    class Campi(str, Enum):
        naturale = "naturale"
        sintetico = "sintetico"
        parquet = "parquet"
        cemento = "cemento"
        palestra = "palestra"
        none = "none"

    campo: Optional[List[Campi]]  # strutture con campi di questo tipo
    is_rated: Optional[bool]  # strutture con almeno una valutazione
    coordinates: Optional[
        Tuple[float, float]
    ]  # necessaria per l'ordinamento secondo vicinanza

    class Costo(IntEnum):
        economico = 5
        medio = 10
        costoso = 15

    costo: Optional[Costo]  # filtro per costo dei campi

    class Order(str, Enum):
        prezzo = "prezzo"
        prezzo_desc = "prezzo_desc"
        rating = "rating"
        rating_desc = "rating_desc"
        vicinanza = "vicinanza"

    ordine: Optional[Order]


@router.post("/list_structures/", response={200: List[int], 404: str})
def list_structures(request, filter: FilterOptions):
    """
    Restituisce tutti gli id delle strutture presenti.<br/>
    Se sono specificati dei filtri, verranno utilizzati<br />
    NOTA: <b>se il filtro è malformato, si restituiranno tutti i risultati.</b>
    """

    def distanza_punti(coord_a, coord_b):
        print("coord_a", coord_a)
        print("coord_b", coord_b)
        # il primo valore è latitudine, il secondo è longitudine
        if (type(coord_a) is not tuple) or (type(coord_b) is not tuple):
            return -1

        try:
            delta_lat = math.pow(coord_a[0] - coord_b[0], 2)
            delta_long = math.pow(coord_a[1] - coord_b[1], 2)
            distanza = math.sqrt(delta_lat + delta_long)
        except Exception:
            return -1

        return distanza

    try:
        if filter.campo:
            filtro_tipo_superficie = (
                Campo.objects.filter(tipo_superficie__in=filter.campo)
                .values("struttura")
                .distinct()
            )
            strutture_filtro_superficie = Struttura.objects.filter(
                id__in=filtro_tipo_superficie
            )
        else:
            strutture_filtro_superficie = Struttura.objects.all()

        if filter.is_rated:
            strutture_filtro_rated = Struttura.objects.filter(
                id__in=Recensione.objects.values("struttura").distinct()
            )
        else:
            strutture_filtro_rated = Struttura.objects.all()

        if filter.costo:
            filtro_costo = (
                Campo.objects.filter(costo_orario__lte=filter.costo)
                .values("struttura")
                .distinct()
            )
            strutture_filtro_costo = Struttura.objects.filter(id__in=filtro_costo)
        else:
            strutture_filtro_costo = Struttura.objects.all()

        strutture_filtro_campo = strutture_filtro_superficie.intersection(
            strutture_filtro_costo
        )
        strutture_filtro = strutture_filtro_campo.intersection(strutture_filtro_rated)

        if filter.ordine:
            if filter.ordine == "prezzo" or filter.ordine == "prezzo_desc":
                strutture_filtro = [
                    (
                        struttura,
                        Campo.objects.filter(struttura=struttura).aggregate(
                            Avg("costo_orario")
                        ),
                    )
                    for struttura in strutture_filtro
                ]

                strutture_filtro.sort(
                    key=lambda struttura: struttura[1],
                    reverse=(filter.ordine == "prezzo_desc"),
                )
                strutture_filtro = [s[0] for s in strutture_filtro]

            elif filter.ordine == "rating" or filter.ordine == "rating_desc":
                strutture_filtro = [
                    (
                        s,
                        Recensione.objects.filter(struttura=s).aggregate(Avg("voto")),
                    )
                    for s in strutture_filtro
                ]
                strutture_filtro = [
                    s for s in strutture_filtro if s[1]["voto__avg"] != None
                ]

                strutture_filtro.sort(
                    key=lambda struttura: struttura[1]["voto__avg"],
                    reverse=(filter.ordine == "rating__desc"),
                )
                strutture_filtro = [s[0] for s in strutture_filtro]

            elif filter.ordine == "vicinanza" and filter.coordinates:
                strutture_filtro = [
                    (s, distanza_punti((s.lat, s.long), filter.coordinates))
                    for s in strutture_filtro
                ]
                strutture_filtro.sort(key=lambda struttura: struttura[1])
                strutture_filtro = [s[0] for s in strutture_filtro]

        return 200, [e.id for e in strutture_filtro]
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
        return 204, None
    except Exception as e:
        return 500, str(e)
