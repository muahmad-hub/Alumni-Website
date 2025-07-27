from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404

import json
from django.template.loader import render_to_string
from channels.db import database_sync_to_async
from datetime import datetime

class MessageConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        from .models import Groups, Members, Messages
        self.user = self.scope['user']
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.group = await database_sync_to_async(get_object_or_404)(
            Groups, 
            group_name=self.group_name
        )

        self.member = await database_sync_to_async(get_object_or_404)(
            Members, 
            group = self.group,
            user = self.user,
        )

        await self.change_online_status(True)
        await self.send_online_status_update()

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print(f"User {self.user} disconnected from group {self.group_name} with close code {close_code}")

        await self.change_online_status(False)
        await self.send_online_status_update()

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        from .models import Groups, Members, Messages
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        new_message = await database_sync_to_async(Messages.objects.create)(
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

    @database_sync_to_async
    def change_online_status(self, is_online):
        self.member.is_online = is_online
        self.member.last_seen = datetime.now()
        self.member.save()

    @database_sync_to_async
    def get_online_count(self):
        from .models import Groups, Members, Messages
        return Members.objects.filter(group=self.group, is_online=True).exclude(user=self.user).count()

    async def send_online_status_update(self):
        online_count = await self.get_online_count()

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'online_status_update',
                'online_count': online_count,
            }
        )

    async def online_status_update(self, event):
        await self.send(text_data=json.dumps({
            'online_count': event['online_count'],
        }))
