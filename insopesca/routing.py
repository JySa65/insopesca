from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
import authentication.consumers

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/notify/', authentication.consumers.NotifyConsumer),
            # chat.routing.websocket_urlpatterns,
            # authentication.routing.websocket_urlpatterns,
        ])
    ),
})
