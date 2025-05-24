import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from buses.models import Bus

class BusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.number_plate = self.scope['url_route']['kwargs']['number_plate']
        normalized_number_plate = self.number_plate.replace(" ", "")
        self.group_name = f"bus_{normalized_number_plate}"

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

        latitude = text_data_json.get('latitude')
        longitude = text_data_json.get('longitude')

        if latitude is not None and longitude is not None:
            # Update the Bus location in DB
            bus = await self.get_bus()
            if bus:
                bus.latitude = latitude
                bus.longitude = longitude
                await self.save_bus(bus)
        else:
            # Fallback for other messages (optional)
            message = text_data_json.get('message')
            if message:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'bus_message',
                        'message': message
                    }
                )

    async def bus_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def location_update(self, event):
        await self.send(text_data=json.dumps({
            'latitude': event['latitude'],
            'longitude': event['longitude'],
        }))

    @database_sync_to_async
    def get_bus(self):
        try:
            return Bus.objects.get(number_plate=self.number_plate)
        except Bus.DoesNotExist:
            return None

    @database_sync_to_async
    def save_bus(self, bus):
        bus.save()
