from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.views.generic.edit import CreateView
class UserForm(UserCreationForm):
    username = forms.EmailField(max_length=255,widget=forms.EmailInput(attrs={"placeholder": "you@example.com", "class": "form-field"}), label="Електронна пошта")
    password1 =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Введи пароль", "class": "form-field password"}),label="Пароль")
    password2 =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Повтори пароль","class": "form-field password"}), label="Підтвердження пароля")

class AuthenticationForm2(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Ім'я користувача або Електронна пошта","class": "form-field"}),label="Ім'я користувача або Електронна пошта")
    password =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Введи пароль", "class": "form-field password"}),label="Пароль")

class ProfileForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "","class": "FormInput firstNameInput"}),label='Ім’я',max_length=255)
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "","class": "FormInput lastNameInput"}),label='Прізвище',max_length=255)
    date_of_birthday = forms.DateField(widget=forms.DateInput(attrs={"type":'date',"placeholder": "", "class":"FormInput DateInput"}), label="Дата народження")
    email = forms.EmailField(max_length=255,widget=forms.EmailInput(attrs={"placeholder": "you@example.com", "class": "FormInput"}), label="Електронна адреса")
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)
        profile=Profile.objects.get(user=self.user)
        self.fields.get('first_name').widget.attrs['value'] = self.user.first_name
        self.fields.get('last_name').widget.attrs['value'] = self.user.last_name
        self.fields.get('email').widget.attrs['value'] = self.user.email
        # self.fields.get('password').widget.attrs['value'] = ''
        self.fields.get('date_of_birthday').widget.attrs['value'] = profile.date_of_birth
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'
            field.widget.attrs['required'] = 'required'
            field.widget.attrs['class'] += ' gray-input'
class PasswordForm(forms.Form):
    old_password =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "••••••••••••••", "class": "FormInput old-password"}),label="Пароль")
    new_password =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "••••••••••••••", "class": "FormInput new-password"}),label= "Новий пароль")
    confirm_new_password =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "••••••••••••••", "class": "FormInput confirm-password"}),label="Підтвердіть новий пароль")

    # def __init__(self, *args, **kwargs):

        # for field_name, field in self.fields.items():
        #     field.widget.attrs['readonly'] = 'readonly'
        #     field.widget.attrs['required'] = 'required'
        #     field.widget.attrs['class'] += ' gray-input'