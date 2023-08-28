from ninja.router import Router
from ninja import ModelSchema, Schema
from typing_extensions import List, Tuple
from struttura.models import Struttura
from django.core.exceptions import ObjectDoesNotExist
from chat.models import Message

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


class MessageSchema(ModelSchema):
    class Config:
        model = Message
        model_exclude = ["id", "struttura", "user"]

    username: str
    room: int


@router.get("/chatMessages/", response={200: List[MessageSchema]})
def get_messages(request, room_id: int = None):
    if not room_id:
        struttura = None
    else:
        try:
            struttura = Struttura.objects.get(id=room_id)
        except Exception as e:
            return 200, []

    messages = Message.objects.filter(struttura=struttura)

    for message in messages:
        username = message.user.username
        message = message.__dict__
        message["username"] = username
        message["room"] = room_id
    return 200, messages
