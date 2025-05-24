from django.contrib import admin
from .models import Bus

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('make', 'capacity', 'number_plate')
    search_fields = ('make', 'number_plate')
    class Meta:
        model = Bus
        fields = '__all__'

