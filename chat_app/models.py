from django.db import models
from django.contrib.auth.models import User
from user_app.models import Profile
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
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='administered_group')
    avatar = models.ImageField(upload_to='images/group_avatars', blank=True, null=True)

    def __str__(self):
        return f'Группа "{self.name}" '
    
    
class ChatMessage(models.Model):
    '''
    Модель для повідомлень
    '''
    content = models.TextField(max_length=4096)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    send_at = models.DateTimeField(auto_now_add=True)
    attached_image = models.ImageField(upload_to="images/messages", blank=True,null=True)

    def __str__(self):
        return f'Повідомлення від {self.author}. Відправлено {self.send_at}'