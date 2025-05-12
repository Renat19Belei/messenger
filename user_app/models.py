from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Code(models.Model):
    code = models.IntegerField(max_length=6)
    date_of_creation = models.DateTimeField(auto_now=True)
    user_id = models.OneToOneField(to=User,on_delete=models.CASCADE)
    # email = models.EmailField(max_length=255)
    # password = models.CharField(max_length=255)
    # username = models.CharField(max_length=255)
    def __str__(self):
        return self.code