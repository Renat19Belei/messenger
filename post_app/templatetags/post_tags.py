from django import template
from post_app.models import Profile,Post
from django.contrib.auth.models import User
register  = template.Library()


@register.inclusion_tag(filename = "post_app/inclusiontags/status.html")
def status(user):
    # friends = Profile.objects.get(user=user).friends.count()
    profile = Profile.objects.get(user=user)
    friends = 0
    # Дописи
    views = 0
    written = 0
    for post in Post.objects.filter(author=profile):
        views += post.views.count()
        written += 1
    
    return {
        "user":user,
        'friends':friends,
        'views':views,
        'written':written
    }