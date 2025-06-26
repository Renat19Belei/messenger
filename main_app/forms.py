from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import PasswordChangeForm
from post_app.models import *
from django.contrib.auth import get_user_model
import re,json
User = get_user_model()

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

            
# >>>>>>> origin/Renat

# class UserPostForm(forms.ModelForm):
#     links = forms.CharField(
#         required=False,
#         widget=forms.Textarea(attrs={
#             'placeholder': 'Введіть посилання через новий рядок',
#             'rows': 3
#         })
#     )

#     class Meta:
#         model = Post
#         fields = ['title', 'tags', 'content', 'images']
# class AlbumForm(forms.ModelForm):
#     class Meta:
#         model = Album
#         fields = ['name', 'created_at', 'topic']