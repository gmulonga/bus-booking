from django.urls import path
from .views import bus_create, bus_list, bus_detail, bus_update, bus_delete

urlpatterns = [
    path('add/', bus_create, name='add_bus'),
    path('get/', bus_list, name='list_buses'),
    path('get/<int:id>/', bus_detail, name='bus_detail'),
    path('update/<int:id>/', bus_update, name='update_bus'),
    path('delete/<int:id>/', bus_delete, name='delete_bus')
]
