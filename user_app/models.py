from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class Code(models.Model):
    code = models.IntegerField()
    date_of_creation = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='codes')
    # email = models.EmailField(max_length=255)
    # password = models.CharField(max_length=255)
    # username = models.CharField(max_length=255)
    def __str__(self):
        return self.code

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    date_of_birth = models.DateField()
    signature = models.ImageField(upload_to="images/signature", blank=True, null=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
#     avatar = models.ImageField(upload_to='images/profiles/avatars')
#     avatar = models.ImageField(upload_to='images/profiles/avatars')
    def __str__(self):
        return self.user.username
class Avatar(models.Model):
    image = models.ImageField(upload_to="images/avatars")
    profile =models.ForeignKey(Profile, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    shown = models.BooleanField(default=True)
    def __str__(self):
        return f'Аватар для профілю {self.profile}'
class Friendship(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friendship_sent_request')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friendship_accepted_request')
    accepted = models.BooleanField(default=False)
    def __str__(self):
        return f'Дружба між {self.profile1} та {self.profile2}'
class VerificationCode(models.Model):
    username = models.CharField(max_length=150)
    code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)