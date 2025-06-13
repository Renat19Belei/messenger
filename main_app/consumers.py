from channels.generic.websocket import AsyncWebsocketConsumer
import json
# from .forms import MessageForm
from channels.db import database_sync_to_async
from .models import ChatGroup, ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    '''
    Обробка WebSocket з'єднання для чату
    '''

    async def connect(self):
        '''
        Підключення до групи чату
        '''
        # Отримуємо pk группи з динамічної url адреси
        self.chat_group_pk = self.scope["url_route"]["kwargs"]["chat_group_pk"]
        # Конвертуємо pk групи в str
        self.group_name = str(self.chat_group_pk)
        # Додаємо канал (тобто користувача) до групи
        await self.channel_layer.group_add(
            # ім'я групи, до якої додаємо канал
            self.group_name,
            # індентифікатор каналу
            self.channel_name 
        )
        # Приймаємо з'єднання
        await self.accept()