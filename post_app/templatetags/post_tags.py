from django import template
from post_app.models import Profile,Post,Link
from user_app.models import Friendship
from django.contrib.auth.models import User
register  = template.Library()


@register.inclusion_tag(filename = "post_app/inclusiontags/status.html")
def status(user):
    # friends = Profile.objects.get(user=user).friends.count()
    profile = Profile.objects.get(user=user)
    friends = Friendship.objects.filter(profile1=profile,accepted=True).count()
    friends += Friendship.objects.filter(profile2=profile,accepted=True).count()
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
@register.inclusion_tag(filename = "post_app/inclusiontags/links.html")
def links(post):

    return {
        "links":Link.objects.filter(post = post)
    }