from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'bus', 'origin', 'destination', 'created_at')
    search_fields = ('booking_id', 'bus__number_plate', 'user__email')

admin.site.register(Booking, BookingAdmin)

