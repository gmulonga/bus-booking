from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/bus/(?P<number_plate>\w+)/$', consumers.BusConsumer.as_asgi()),
]