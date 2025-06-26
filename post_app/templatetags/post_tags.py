from django import template
from post_app.models import Profile,Post,Link,Tag
from user_app.models import Friendship
register  = template.Library()

# Включаемый тег для отображения статистики пользователя (друзья, просмотры, количество постов)
@register.inclusion_tag(filename = "post_app/inclusiontags/status.html")
def status(user):
    profile = Profile.objects.get(user=user)
    # Считаем количество друзей (в обе стороны)
    friends = Friendship.objects.filter(profile1=profile,accepted=True).count()
    friends += Friendship.objects.filter(profile2=profile,accepted=True).count()
    views = 0
    written = 0
    # Считаем количество просмотров и написанных постов
    for post in Post.objects.filter(author=profile):
        views += post.views.count()
        written += 1
    return {
        "user":user,
        'friends':friends,
        'views':views,
        'written':written
    }

# Включаемый тег для отображения ссылок, прикрепленных к посту
@register.inclusion_tag(filename = "post_app/inclusiontags/links.html")
def links(post):
    return {
        "links":Link.objects.filter(post = post)
    }

# Список стандартных тегов для постов
standard_tags_list = '#відпочинок #натхенення #життя #природа #читання #спокій #гармонія #музика #фільми #подорожі'.split(' ')

# Включаемый тег для отображения стандартных тегов (создает их, если не существуют)
@register.inclusion_tag(filename = "post_app/inclusiontags/standard_tags.html")
def standard_tags():
    tags = []
    for standard_tag in standard_tags_list:
        tag = Tag.objects.filter(name = standard_tag).first()
        if tag == None:
            tags.append( Tag.objects.create(name = standard_tag))
        else:
            tags += [tag]
    return {'tags':tags}