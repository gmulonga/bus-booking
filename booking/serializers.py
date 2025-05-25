from rest_framework import serializers
from .models import Booking
from buses.models import Bus
from users.models import User

class BookingSerializer(serializers.ModelSerializer):
    bus = serializers.CharField(write_only=True)
    bus_details = serializers.SerializerMethodField(read_only=True)
    user_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'booking_id', 'user_details', 'origin', 'destination', 'bus', 'bus_details', 'created_at']
        read_only_fields = ['user', 'booking_id', 'created_at']

    def get_bus_details(self, obj):
        return {
            "id": obj.bus.id,
            "number_plate": obj.bus.number_plate
        }

    def get_user_details(self, obj):
        user = obj.user
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }

    def create(self, validated_data):
        bus_number_plate = validated_data.pop('bus')
        bus = Bus.objects.filter(number_plate=bus_number_plate).first()
        if not bus:
            raise serializers.ValidationError({"bus": "Bus with this number plate does not exist."})

        user = self.context['request'].user
        booking = Booking.objects.create(
            user=user,
            bus=bus,
            **validated_data
        )
        return booking
