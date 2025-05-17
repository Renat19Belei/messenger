from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from user_app.models import *
from django.contrib.auth import get_user_model

User = get_user_model()
class messageForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Текст публікації","class": "input"}),max_length=2000)
    # def send(self, commit=True):
    #     instance = super().send(commit=False)
    #     instance.user = self.user
    #     if self.user and self.user.is_authenticated:
    #         User_Post.objects.create(
    #             text=self.cleaned_data.get('text'),
    #             user = self.user,
    #             reviewers = 0,
    #             likes = 0
    #             )
    #     print('heeheheh')
    #     return super().form_valid(form)
        # user  = models.OneToOneField(to=User, on_delete= models.CASCADE)
        # name = models.CharField(max_length=255)
        # theme = models.CharField(max_length=255,null=True)
        # tags  = models.ManyToManyField(to=Tags)
        # text = models.TextField()
        # link  = models.CharField(max_length=255)
        # images = models.ManyToManyField(to=Images)
        # reviewers = models.IntegerField()
        # likes