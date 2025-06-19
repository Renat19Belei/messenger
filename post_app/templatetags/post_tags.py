from django import template
from post_app.models import Profile,Post,Link,Tag
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
standard_tags_list = '#відпочинок #натхенення #життя #природа #читання #спокій #гармонія #музика #фільми #подорожі'.split(' ')
# @register.simple_tag(name= "standard_tags")
@register.inclusion_tag(filename = "post_app/inclusiontags/standard_tags.html")
def standard_tags():
    # Tag.objects.filter
    tags = []
    for standard_tag in standard_tags_list:
        tag = Tag.objects.filter(name = standard_tag).first()
        if tag == None:
            tags.append( Tag.objects.create(name = standard_tag))
        else:
            tags += [tag]
    
    # print(tags)
    # if standard_tags_list > tags.count():
    #     for standard_tag in standard_tags_list:
            
    for count in range(111):
        print(tags)
    return {'tags':tags}