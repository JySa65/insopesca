from django.urls import path, re_path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.consumers
import authentication.consumers

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/notify/', authentication.consumers.NotifyConsumer),
            re_path(
                r'^ws/chat/(?P<room_name>[^/]+)/$', chat.consumers.ChatConsumer),
            # path('ws/chat/<str:room_name>', chat.consumers.ChatConsumer)
        ])
    ),
})
