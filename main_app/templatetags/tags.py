from django import template
from user_app.models import Profile,Avatar
register  = template.Library()

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
    else:
        profile = Profile.objects.get(user=user)
    avatar = Avatar.objects.filter(profile=profile,shown=True,active=True).first()
    return {'avatar':avatar,'class':clas}

@register.inclusion_tag(filename = "main_app/inclusiontags/friends_cards.html")
def friends_cards(users,text= 'Підтвердити'):
    
    return {"users":users, "text": text}