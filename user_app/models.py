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

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
#     avatar = models.ImageField(upload_to='images/profiles/avatars')
#     avatar = models.ImageField(upload_to='images/profiles/avatars')