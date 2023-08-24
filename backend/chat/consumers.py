import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from chat.models import Message
from struttura.models import Struttura


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if not isinstance(user, User):
            print("Utente anonimo, connessione rifiutata")
            return False

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]
        room = int(self.scope["url_route"]["kwargs"]["room_name"])

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

        await self.save_message(room=room, message=message, user=user)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def save_message(self, room, message, user):
        if room > 0:
            room = Struttura.objects.get(id=room)
        else:
            room = None  # lobby generale
        try:
            Message.objects.create(struttura=room, message=message, user=user)
            print("messaggio salvato nel DB.")
        except Exception as e:
            print("Errore, messaggio non salvato nel DB.")
