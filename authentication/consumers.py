# chat/consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotifyConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("events", self.channel_name)
        # print(f"Added {self.channel_name} channel to events")

    async def disconnect(self, message):
        await self.channel_layer.group_discard("events", self.channel_name)
        # print(f"Removed {self.channel_name} channel to events")

    async def events_alarms(self, event):
        data = dict(
            msg=event.get('message', '')
        )
        await self.send_json(data)
        print(f"Got message {event} at {self.channel_name}")

