from channels.generic.websocket import AsyncWebsocketConsumer
import json, base64
from channels.db import database_sync_to_async

from django.core.files.base import ContentFile
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
    async def receive(self, text_data):
        '''
        Отримання і збереження повідомлення
        '''
        # Отримуємо поточного користувача
        self.user = self.scope["user"]
        loads_text_data = json.loads(text_data)
        # Отримуємо ім'я поточного користувача
        first_name = self.user.first_name
        last_name = self.user.last_name
        # Зберігаємо повідомлення у базу даних та у цю змінну
        django_file=None
        imgType = loads_text_data.get('imgType')
        if imgType:
            img = base64.b64decode(loads_text_data.get('img'))
            django_file = ContentFile(img, name=f'fileo.{imgType}')
        saved_message = await self.save_message(message = loads_text_data['message'],attached_image=django_file)
        message_pk = saved_message.pk
        # Надсилаємо повідомлення у группу
        await self.channel_layer.group_send(
            # ім'я группи, до якої відправляємо повідомлення
            self.group_name,
            {
                # Вказуємо тип події (ім'я методу що відпрацює для кожного учасника групи)
                "type": "send_message_to_chat",
                # Дані, що передаємо у send_message_to_chat через параметр event
                "text_data": text_data,
                'message_pk':message_pk,
                'userous_pk':self.user.pk,
                'img':saved_message.attached_image,
                "date_time": saved_message.send_at,
                "username": first_name + ' ' + last_name
            }
        )
    
    async def send_message_to_chat(self, event):
        '''
        Метод, який відправляє повідомлення у чат
        '''
        # Перетворюємо json рядок з повідомленням у словник
        text_data_dict = json.loads(event["text_data"])
        # отримаємо ім`я відправника
        username = event["username"]
        if event['img']:
            text_data_dict['img'] = event["img"].url
        # задання для text_data_dict ім'я користувача
        text_data_dict['username'] = username
        # задання для text_data_dict дату відправки в iso форматі
        text_data_dict["date_time"] = event["date_time"].isoformat()
        # self.group_name
        text_data_dict['you'] = 1
        if self.scope["user"].pk!=event['userous_pk']:
            text_data_dict['you'] = 0
            text_data_dict['avatar'] = await self.get_avatar(event['userous_pk'])
        # відправка текст дати у json форматі клієнтам
        await self.send(json.dumps(text_data_dict))
    @database_sync_to_async
    def get_avatar(self, user_pk):
        
        from user_app.models import Profile,Avatar
        profile = Profile.objects.filter(user_id=user_pk).first()
        avatar = Avatar.objects.filter(profile=profile,active=True,shown=True).first()
        if avatar:
            avatar = avatar.image.url
        # else:
        #     avatar = None
        return avatar
    @database_sync_to_async
    def save_message(self, message,attached_image=None):
        '''
        метод,який потрібен для збереження повідомлення у БД
        '''
        from .models import ChatGroup, ChatMessage
        # задаємо автора 
        author = self.scope['user']
        # задаємо повідомлення 
        message = message
        # отримуємо та записуємо у змінну об'єкт групи
        group = ChatGroup.objects.get(pk = self.group_name)
        # зберігаємо і повертаємо створений об'єкт повідомлення
        messageObject = ChatMessage.objects.create(author = author, content = message, chat_group = group)
        if attached_image:
            messageObject.attached_image = attached_image
            messageObject.save()
        return messageObject