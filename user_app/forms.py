from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
class UserForm(UserCreationForm):
    # username = forms.CharField(max_length=255)
    # password = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    # def save(self):
        
    #     user = User.objects.create(
    #         username=self.cleaned_data["username"],
    #         password=self.cleaned_data["password"],
    #         email=self.cleaned_data["email"]
    #     )
    pass