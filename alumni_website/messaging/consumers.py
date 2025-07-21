from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import MessageGroup, GroupMessage
import json
from django.template.loader import render_to_string
from channels.db import database_sync_to_async

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.group = await database_sync_to_async(get_object_or_404)(
            MessageGroup, group_name=self.group_name
        )

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        new_message = await database_sync_to_async(GroupMessage.objects.create)(
            group=self.group,
            sender=self.user,
            message=message
        )

        data = await database_sync_to_async(render_to_string)(
            'messaging/partials/chat_message.html', {
                'message': new_message,
                'user': self.user,
                'sender': new_message.sender,
            }
        )

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': new_message.message,
                'sender_id': self.user.id,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
        }))
