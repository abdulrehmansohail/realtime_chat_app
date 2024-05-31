from .consumers import (
    ChatUpdateConsumers,
    DashboardChatConsumer,
    GroupActivityAsyncConsumer,

)
from django.urls import path


websocket_urlpatterns = [
    # Private Chat
    path('api/dashboard/chat/', DashboardChatConsumer.as_asgi()),
    path('api/chat/update/', ChatUpdateConsumers.as_asgi()),
    # Group Chat
    path('api/group/activity/chat/', GroupActivityAsyncConsumer.as_asgi()),
]
