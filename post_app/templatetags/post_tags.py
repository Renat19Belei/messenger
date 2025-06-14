from django import template
from main_app.models import Profile,User_Post
from django.contrib.auth.models import User
register  = template.Library()


@register.inclusion_tag(filename = "post_app/inclusiontags/status.html")
def status(user):
    friends = Profile.objects.get(user=user).friends.count()
    # Дописи
    views = 0
    written = 0
    for post in User_Post.objects.filter(user=user):
        views += post.reviewers.count()
        written += 1
    
    return {
        "user":user,
        'friends':friends,
        'views':views,
        'written':written
    }