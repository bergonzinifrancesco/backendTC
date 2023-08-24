from ninja.router import Router
from ninja.schema import Schema
from typing_extensions import List, Tuple
from struttura.models import Struttura
from django.core.exceptions import ObjectDoesNotExist

router = Router(tags=["Chat"])


class RoomSchema(Schema):
    id: int
    nome: str


@router.get("/rooms/", response={200: List[RoomSchema]})
def get_rooms(request):
    rooms = [{"id": 0, "nome": "Generale"}]
    try:
        strutture = Struttura.objects.values("id", "nome")
    except ObjectDoesNotExist:
        print("Non ci sono strutture")
    rooms.extend(strutture)
    return 200, rooms
