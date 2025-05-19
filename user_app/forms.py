from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
class UserForm(UserCreationForm):
    # username = forms.CharField(max_length=255)
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "ім'я","class": "form-field"}),label="Ім'я користувача ")
    password1 =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Введи пароль", "class": "form-field password"}),label="Пароль")
    password2 =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Повтори пароль","class": "form-field password"}), label="Підтвердження пароля")
    # 
    email = forms.EmailField(max_length=255,widget=forms.EmailInput(attrs={"placeholder": "you@example.com", "class": "form-field"}), label="Ємаіл")
    # def save(self):
    #     user = User.objects.create(
    #         username=self.cleaned_data["username"],
    #         password=self.cleaned_data["password1"],
    #         email=self.cleaned_data["email"],
    #         is_active = False
    #     )
        
    #     return user