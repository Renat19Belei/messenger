from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
    user  = models.ForeignKey(to=User, on_delete= models.CASCADE)
    name = models.CharField(max_length=255)
    theme = models.CharField(max_length=255,null=True)
    tags  = models.ManyToManyField(to=Tags)
    text = models.TextField()
    # link  = models.CharField(max_length=255, null=True)
    links  = models.ManyToManyField(to=Link)
    images = models.ManyToManyField(to=Images)
    reviewers = models.IntegerField()
    likes = models.IntegerField()
    def clean(self):
        ok = super().clean()
        if self.tags.count()>9: 
            raise ValidationError("Максимальна кількість тегів дорівнює 9")
        return ok
class Album(models.Model):
    image = models.ImageField(upload_to="album")
    name = models.CharField(max_length=255)
    year = models.DateField(blank= True,null=True)
    theme = models.CharField(max_length=255)

class Profile(models.Model):
    icon = models.ImageField(upload_to= "profile/")
    birthday = models.DateField(blank= True,null=True)
    user = models.OneToOneField(to = User, on_delete= models.CASCADE)
    album = models.ForeignKey(to=Album, on_delete= models.CASCADE,null=True)
    electronicSignature = models.ImageField(upload_to= "images/electronicSignature/")



    
# <<<<<<< Renat
class Link(models.Model):
    url = models.URLField()
    description = models.CharField(max_length=255, blank=True)
    post = models.ForeignKey(User_Post, related_name='links', on_delete=models.CASCADE)

    def __str__(self):
        return self.url
# =======
# >>>>>>> master
