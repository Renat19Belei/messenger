from django import template
from user_app.models import Profile,Avatar
register  = template.Library()
from django.utils import timezone 
from chat_app.models import ChatGroup,ChatMessage
# contact.html
# @register.inclusion_tag(filename = "main_app/inclusiontags/contact.html")
# def render_header(pk):
#     chatMessage =ChatMessage.objects.filter(pk=pk).order_by('-send_at').first()
#     ChatGroup.objects.filter()
@register.inclusion_tag(filename = "main_app/inclusiontags/header.html")
def render_header(main=0, posts=0, friends=0, chats=0, personal=0):
    pages = {
        "main": main,
        "posts": posts,
        "friends": friends,
        "chats": chats,
        "personal": personal
    }
    for page in pages:
        if int(pages[page])==1:
            pages[page] = "current-page"
        else:
            pages[page] = ''
    # 
    return pages
# 'profile_icon':profile.icon

# users
@register.inclusion_tag(filename = "main_app/inclusiontags/profile_icon.html")
def profile_icon(user, clas = 'avatar'):
    # Avatar
    
    if type(user)==type(131):
        profile = Profile.objects.get(user_id=user)
    elif type(user)==type(Profile):
        pass
    else:
        profile = Profile.objects.get(user=user)
    avatar = Avatar.objects.filter(profile=profile,shown=True,active=True).first()
    return {'avatar':avatar,'class':clas}

@register.inclusion_tag(filename = "main_app/inclusiontags/friends_cards.html")
def friends_cards(users,text= 'Підтвердити'):
    
    return {"users":users, "text": text}
@register.simple_tag(name = 'currentTime')
def currentTime():
    
    return timezone.now().hour