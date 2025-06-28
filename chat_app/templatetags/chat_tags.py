from django import template
from user_app.models import Profile,Avatar
from django.utils import timezone 
register  = template.Library()
from chat_app.models import ChatGroup,ChatMessage

def contact_create(request,pk):
    """Функция для получения данных контакта по его первичному ключу (pk).
    Параметры:
    - request: объект запроса
    - pk: первичный ключ сообщения
    """
    if pk:
        # Получаем последнее сообщение по pk
        message = ChatMessage.objects.filter(pk=pk).order_by('-send_at').first()
        # Получаем группу чата, к которому относится сообщение
        chat_group = message.chat_group
        # Получаем собеседника (друга), исключая текущего пользователя
        friend = chat_group.members.exclude(user=request.user).first()
        # Получаем активный аватар собеседника
        avatar = Avatar.objects.filter(active = True, profile = friend).first()
        # Форматируем время отправки сообщения
        time_text = message.send_at.isoformat()
        # Возвращаем данные для шаблона
        return {
            "username": friend.user.first_name + ' ' + friend.user.last_name,
            "messageText": message.content, 
            "time_text": time_text,
            "message": message,
            "avatar": avatar,
            'pk': friend.pk
        }
    # Включаемый тег для отображения контакта в списке чатов (contact.html)
@register.inclusion_tag(filename = "chat_app/inclusion_tags/contact_tag.html")
def contact_tag(request,pk):
    return contact_create(request,pk)
@register.inclusion_tag(filename = "chat_app/inclusion_tags/contact_main_tag.html")
def contact_main_tag(request,pk):
    return contact_create(request,pk)