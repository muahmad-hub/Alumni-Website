from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/message/<str:group_name>/', MessageConsumer.as_asgi()),
]