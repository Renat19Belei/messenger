from django import template
from user_app.models import Profile,Avatar
from django.utils import timezone 
register  = template.Library()
from chat_app.models import ChatGroup,ChatMessage
# contact.html
@register.inclusion_tag(filename = "chat_app/inclusion_tags/contact.html")
def contact(request,pk):
    message = ChatMessage.objects.filter(pk=pk).order_by('-send_at').first()
    chat_group =message.chat_group
    friend=chat_group.members.exclude(user=request.user).first()
    
    now = timezone.now()
    avatar = Avatar.objects.filter(active = True, profile = friend).first()
    time_text = ""
    if message.send_at.day == now.day:
        # 09:41 
        print('ok')
        time_text = f"{message.send_at.hour}:{message.send_at.minute}" 
    else:
        # 25.04.2025
        print('ewqweqewq')
        time_text = f"{message.send_at.day}.{message.send_at.month}.{message.send_at.year}"
    print(time_text)
    return {
        "username": friend.user.first_name,
        "message": message.content, 
        "time_text": time_text,
        "avatar": avatar
            }