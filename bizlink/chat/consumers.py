from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from .models import ChatGroup, GroupMessage
import json

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_id = self.scope['url_route']['kwargs']['chatGroupId']  # Use chatGroupId
        self.chatroom = get_object_or_404(ChatGroup, chatGroupId=self.chatroom_id)  # Get chat group by ID
        print(f"Connecting to chatroom: {self.chatroom_id}")  

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_id,  # Use chatGroupId for the channel layer group name
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_id,  # Use chatGroupId
            self.channel_name
        )
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        message = GroupMessage.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom
        )

        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_id,  # Use chatGroupId
            event
        )
    
    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)

        html = render_to_string("chat/partials/chat_message_p.html", {
            'message': message,
            'user': self.user,
        })

        self.send(text_data=html)