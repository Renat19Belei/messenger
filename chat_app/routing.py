from django.urls import path
from .consumers import ChatConsumer

#Створюємо список з шляхами по веб-сокет з'єднанню
websocket_urlpatterns = [
    #Вказуємо диманічний шлях до групи за допомогою її pk
    path("chat_group/<int:chat_group_pk>", ChatConsumer.as_asgi())
]