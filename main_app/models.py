from django.db import models
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError
from django.conf import settings
# Create your models here.
class Tags(models.Model):
    name = models.CharField(max_length=100)
    # posts = models.ManyToManyField(to=User_Post)
class Images(models.Model):
    image = models.ImageField(upload_to="images")
class Link(models.Model):
    url = models.URLField()
    # description = models.CharField(max_length=255, blank=True)
    # post = models.ForeignKey(User_Post, related_name='links', on_delete=models.CASCADE)

    def __str__(self):
        return self.url

class User_Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    name = models.CharField(max_length=255)
    theme = models.CharField(max_length=255,null=True)
    tags  = models.ManyToManyField(to=Tags)
    text = models.TextField()
    # link  = models.CharField(max_length=255, null=True)
    links  = models.ManyToManyField(to=Link)
    images = models.ManyToManyField(to=Images)
    reviewers = models.ManyToManyField(blank=True,to=User)
    likes = models.IntegerField()
    def clean(self):
        ok = super().clean()
        if self.tags.count()>9: 
            raise ValidationError("Максимальна кількість тегів дорівнює 9")
        return ok
# class Album(models.Model):
#     image = models.ImageField(upload_to="album")
#     name = models.CharField(max_length=255)
#     year = models.DateField(blank= True,null=True)
#     theme = models.CharField(max_length=255)

class Profile(models.Model):
    icon = models.ImageField(upload_to= "profile/",null=True,blank=True)
    birthday = models.DateField(blank= True,null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    # album = models.ManyToManyField(to=Album,blank=True)
    name_view = models.BooleanField(default=True)
    electronicSignature_view = models.BooleanField(default=False)
    electronicSignature = models.ImageField(upload_to= "images/electronicSignature/",null=True,blank=True)
    friends = models.ManyToManyField(to="self", blank=True, symmetrical=True)

class Album(models.Model):
    images = models.ManyToManyField(to=Images,blank= True)
    name = models.CharField(max_length=255)
    year = models.IntegerField(blank= True,null=True)
    theme = models.CharField(max_length=255)
    user = models.ForeignKey(to=User,on_delete=models.CASCADE, related_name='user')

# class CustomUser(AbstractUser):
#     pass
    
# <<<<<<< Renat
# class Link(models.Model):
#     url = models.URLField()
#     description = models.CharField(max_length=255, blank=True)
#     post = models.ForeignKey(User_Post, related_name='links', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.url
# =======
# >>>>>>> master
class ChatGroup(models.Model):
    '''
    Модель ChatGroup, в якій зберігаються Chat-групи
    '''
    name = models.CharField(max_length = 255)
    users = models.ManyToManyField(User)
    personal_chat = models.BooleanField(default = False)
    
    
class ChatMessage(models.Model):
    '''
    Модель для повідомлень
    '''
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    views = models.ManyToManyField(User, related_name='viewed_messages')
    images = models.ManyToManyField(to=Images, blank=True)