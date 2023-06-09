# main/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from main.models import *

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "room_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = text_data_json['user']
        Message.objects.create(
            user=User.objects.get(username=user),
            text = message,
            room = ChatRoom.objects.get(id=Friend.objects.get(id=self.room_name))
        ).save()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message, "user":user}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        prof_obj = Profile.objects.get(username=User.objects.get(username=str(user)))
        dp = prof_obj.display_picture.url
        first_name = prof_obj.first_name
        last_name = prof_obj.first_name
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, 'user':user, 'dp':dp, 'first_name':first_name, 'last_name':last_name}))
