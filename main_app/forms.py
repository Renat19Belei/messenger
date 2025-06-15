from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from .models import *
from django.contrib.auth import get_user_model
import re,json
User = get_user_model()
class messageForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Напишіть назву публікації","class": "FormInput nameInput"}),label='Назва публікації',max_length=255)
    theme = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Напишіть тему публікаціїї","class": "FormInput themeInput"}),label='Тема публікації',max_length=255, required=False)

    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Напишіть текст публікації","class": "BigFormInput textInput"}),label='',max_length=2000)

    #     
    def send(self, user, images,type = 'save',imgs=[],remove_List=[[],[]],tags=[],links = []):
        print(user)
        if user and user.is_authenticated:
                
            images_list = []
            tags_list = []
            try:
                count = 0
                for img in json.loads(imgs):
                    if not (str(count) in remove_List[1]):
                        images_list += [Images.objects.get(pk=int(img))]
                    count+= 1
                
            except Exception as error:
                print(error)
            try:
                count =0
                for image in images:
                    if not (str(count) in remove_List[0]):
                        images_list += [Images.objects.create(image=image)]
                    count+=1
            except Exception as error:
                print(error)
            text = self.cleaned_data.get('text')
            for tag in tags:
                tag = tag[1::]
                tags_list.append(Tags.objects.create(name= tag))
            link_list = []
            for link in links:
                link_list += [Link.objects.create(url=link)]
                # text = "".join(text.split('#'+tag))
            if type == 'save':
                
                user_post = User_Post.objects.create(
                    text=text,
                    user = user,
                    # reviewers = 0,
                    likes = 0,
                    name = self.cleaned_data.get('name'),
                    theme = self.cleaned_data.get('theme'),
                    # link = self.cleaned_data.get('link'),
                )
                user_post.images.set(images_list)
                user_post.tags.set(tags_list)
                user_post.links.set(link_list)
                
                user_post.save()
                # for link in links:
                #     lonk = Link.objects.create(url=link,post=user_post)
                    

                # for count in range(132):
                #     print(user_post.name)
            else:
                
                user_post = User_Post.objects.get(
                    pk=type
                )
                if user_post.user == user:
                    user_post.text = text
                    user_post.name = self.cleaned_data.get('name')
                    user_post.theme = self.cleaned_data.get('theme')
                    # user_post.link = self.cleaned_data.get('link')
                    user_post.images.set(images_list)
                    user_post.tags.set(tags_list)
                    user_post.save()
                
        print('heehehewqsxcvbnm')
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
class UserSet(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Введіть Ваше ім’я","class": "FormInput firstNameInput"}),label='Ім’я',max_length=255)
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Введіть Ваше прізвище","class": "FormInput lastNameInput"}),label='Прізвище',max_length=255)
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "@","class": "FormInput lastNameInput"}),label='Ім’я користувача',max_length=255)  
    def save(self,user):
        print('gwewgeg')
        user.email = user.username
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username = self.cleaned_data.get('username')
        user.save()
class ProfileForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "","class": "FormInput firstNameInput"}),label='Ім’я',max_length=255)
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "","class": "FormInput lastNameInput"}),label='Прізвище',max_length=255)
    date_of_birthday = forms.DateField(widget=forms.DateInput(attrs={"type":'date',"placeholder": "", "class":"FormInput DateInput"}), label="Дата народження")
    
# <<<<<<< HEAD
    email = forms.EmailField(max_length=255,widget=forms.EmailInput(attrs={"placeholder": "you@example.com", "class": "FormInput"}), label="Електронна адреса")
    password =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "***********", "class": "FormInput password"}),label="Пароль")
# =======
#     email = forms.EmailField(max_length=255,widget=forms.EmailInput(attrs={"placeholder": "you@example.com", "class": "FormInput"}), label="Електронна адреса")
#     password =forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "***********", "class": "FormInput password"}),label="Пароль")
    # def save(self, user):
    #     self.user = user
        
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        profile=Profile.objects.get(user=self.user)
        print(profile.pk,profile.user,profile.birthday)
        self.fields.get('first_name').widget.attrs['value'] = self.user.first_name
        self.fields.get('last_name').widget.attrs['value'] = self.user.last_name
        self.fields.get('email').widget.attrs['value'] = self.user.email
        self.fields.get('password').widget.attrs['value'] = '••••••••••••••'
        print(profile.birthday,67890-909987565432)
        self.fields.get('date_of_birthday').widget.attrs['value'] = profile.birthday
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'
            field.widget.attrs['required'] = 'required'
            field.widget.attrs['class'] += ' gray-input'
# >>>>>>> origin/Renat

class UserPostForm(forms.ModelForm):
    links = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Введіть посилання через новий рядок',
            'rows': 3
        })
    )

    class Meta:
        model = User_Post
        fields = ['name', 'theme', 'tags', 'text', 'images']
class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'year', 'theme']