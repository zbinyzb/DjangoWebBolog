import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

# 这是来自 routing.py 的内容，自此 routing.py 废弃
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import blog.routing

application = ProtocolTypeRouter({
    #(http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            blog.routing.websocket_urlpatterns
        )
    ),
})
