from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
class Tags(models.Model):
    name = models.CharField(max_length=100)
    # posts = models.ManyToManyField(to=User_Post)
class Images(models.Model):
    image = models.ImageField(upload_to="images")
class User_Post(models.Model):
    user  = models.OneToOneField(to=User, on_delete= models.CASCADE)
    name = models.CharField(max_length=255)
    theme = models.CharField(max_length=255,null=True)
    tags  = models.ManyToManyField(to=Tags,null=True)
    text = models.TextField()
    link  = models.CharField(max_length=255)
    images = models.ManyToManyField(to=Images,null=True)
    reviewers = models.IntegerField()
    likes = models.IntegerField()
    def clean(self):
        ok = super().clean()
        if self.tags.count()>9: 
            raise ValidationError("Максимальна кількість тегів дорівнює 9")
        return ok