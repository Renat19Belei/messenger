from django.db import models
from django.contrib.auth.models import User
from main_app.models import Profile, Images
# Create your models here.
# class messageForm(models.Model):
#     text = 
#     image = 
class ChatGroup(models.Model):
    '''
    Модель ChatGroup, в якій зберігаються Chat-групи
    '''
    name = models.CharField(max_length = 255)
    members = models.ManyToManyField(Profile, blank=True)
    is_personal_chat = models.BooleanField(default = False)
    
    
class ChatMessage(models.Model):
    '''
    Модель для повідомлень
    '''
    content = models.TextField(max_length=4096)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    send_at = models.DateTimeField(auto_now_add=True)
    attached_image = models.ImageField(upload_to="images/messages", blank=True,null=True)