from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()
class messageForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Текст публікації","class": "input"}),max_length=2000)
    def send(self, user):
        print(user)
        if user and user.is_authenticated:
            User_Post.objects.create(
                text=self.cleaned_data.get('text'),
                user = user,
                reviewers = 0,
                likes = 0,
                name = user.username
                )
            print('heeheheh')
        # return super().form_valid(form)
        # user  = models.OneToOneField(to=User, on_delete= models.CASCADE)
        # name = models.CharField(max_length=255)
        # theme = models.CharField(max_length=255,null=True)
        # tags  = models.ManyToManyField(to=Tags)
        # text = models.TextField()
        # link  = models.CharField(max_length=255)
        # images = models.ManyToManyField(to=Images)
        # reviewers = models.IntegerField()
        # likes