from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("", views.chat, name="chat"),
    path("chatroom/<chatGroupId>/", views.chatroom, name="chatroom"),
    path("get_or_create_chatroom/<username>/", views.get_or_create_chatroom, name="get_or_create_chatroom"),
    path('unread-count/<chatGroupId>/', views.unread_message_count, name='unread_message_count'),
]