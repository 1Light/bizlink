from django.urls import path
from .consumers import ChatroomConsumer

app_name = "chat"

websocket_urlpatterns = [
    path("ws/chatroom/<str:chatGroupId>/", ChatroomConsumer.as_asgi()),
]