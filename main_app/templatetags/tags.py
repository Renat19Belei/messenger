from django import template

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