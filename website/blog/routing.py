from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    # url(r'^ws/chat/(?p<root_name>[^/]+)/$',consumers.ChatConsumer),
    # url(r'^chat-channel/',consumers.ChatConsumer),
    url(r'^chat-channel/',consumers.ChatConsumer.as_asgi()),
    
]