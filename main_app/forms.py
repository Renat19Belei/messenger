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
class PasswordForm(forms.Form):
    old_password =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "••••••••••••••", "class": "FormInput old-password"}),label="Пароль")
    new_password =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "••••••••••••••", "class": "FormInput new-password"}),label= "Новий пароль")
    confirm_new_password =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "••••••••••••••", "class": "FormInput confirm-password"}),label="Підтвердіть новий пароль")
    
class ProfileForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "","class": "FormInput firstNameInput"}),label='Ім’я',max_length=255)
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "","class": "FormInput lastNameInput"}),label='Прізвище',max_length=255)
    date_of_birthday = forms.DateField(widget=forms.DateInput(attrs={"type":'date',"placeholder": "", "class":"FormInput DateInput"}), label="Дата народження")
    
# <<<<<<< HEAD
    email = forms.EmailField(max_length=255,widget=forms.EmailInput(attrs={"placeholder": "you@example.com", "class": "FormInput"}), label="Електронна адреса")
    # password =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "***********", "class": "FormInput password"}),label="Пароль")
# =======
#     email = forms.EmailField(max_length=255,widget=forms.EmailInput(attrs={"placeholder": "you@example.com", "class": "FormInput"}), label="Електронна адреса")
#     password =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "***********", "class": "FormInput password"}),label="Пароль")
    # def save(self, user):
    #     self.user = user
        
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        profile=Profile.objects.get(user=self.user)
        # print(profile.pk,profile.user,profile.date_of_birth)
        self.fields.get('first_name').widget.attrs['value'] = self.user.first_name
        self.fields.get('last_name').widget.attrs['value'] = self.user.last_name
        self.fields.get('email').widget.attrs['value'] = self.user.email
        # self.fields.get('password').widget.attrs['value'] = '••••••••••••••'
        print(profile.date_of_birth,67890-909987565432)
        self.fields.get('date_of_birthday').widget.attrs['value'] = profile.date_of_birth
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'
            field.widget.attrs['required'] = 'required'
            field.widget.attrs['class'] += ' gray-input'
            
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