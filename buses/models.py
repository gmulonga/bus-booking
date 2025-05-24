from django.db import models
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class Bus(models.Model):
    make = models.CharField(max_length=100)
    number_plate = models.CharField(max_length=20, unique=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    capacity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.make} - {self.number_plate}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_latitude = None
        old_longitude = None

        if not is_new:
            old_bus = Bus.objects.get(pk=self.pk)
            old_latitude = old_bus.latitude
            old_longitude = old_bus.longitude

        super(Bus, self).save(*args, **kwargs)

        if (self.latitude != old_latitude or self.longitude != old_longitude) or is_new:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'bus_{self.number_plate.replace(" ", "")}',
                {
                    'type': 'location_update',
                    'latitude': self.latitude,
                    'longitude': self.longitude,
                }
            )
