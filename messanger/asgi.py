"""
ASGI config for messanger project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat_app.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messanger.settings')

application = ProtocolTypeRouter({
    # Якщо звичайний http запит, тоді звичайна обробка запиту django
    'http': get_asgi_application(),
    # Якщо websocket запит
    'websocket': AuthMiddlewareStack( # AuthMiddlewareStack дає доступ до об'єкта аввторизованого користувача через self.scope у ChatConsumer
        URLRouter(websocket_urlpatterns) # Вказуємо файл з маршрутизацією для обробки websocket-запитів
    )
})