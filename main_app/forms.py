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
    text = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Напишіть текст публікації","class": "BigFormInput textInput"}),label='',max_length=2000)
    link = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Вставте посилання публікації","class": "formInput linkInput"}),label='Посилання',max_length=255, required=False)
    # images = forms.ImageField(widget=forms.HiddenInput(attrs={"id":"imageInput","type":"file", "accept":"image/*", "multiple":True}))
    #     
    def send(self, user, images,type = 'save',imgs=[]):
        print(user)
        if user and user.is_authenticated:
                
            images_list = []
            tags_list = []
            print(imgs.split(','))
            try:
                for img in json.loads(imgs):
                    images_list += [Images.objects.get(pk=int(img))]
                
            except Exception as error:
                print(error)
            try:
                for image in images:
                    images_list += [Images.objects.create(image=image)]
            except Exception as error:
                print(error)
            text = self.cleaned_data.get('text')
            # print('3212213213'.startswith('2'))
            # tags = re.findall("#(\w+)", text)
            # text = '#hhhh hello #hi '
            text_list = []
            tags = []
            tags2 = text.split(' ')
            # tags_list = []
            for tag in tags2:
                if tag.startswith('#'):
                    t = tag[1::]
                    tags.append(t)
                else:
                    text_list.append(tag)
            
            text = ' '.join(text_list)
            # print(tags_list)
            # tags
            for tag in tags:
                tags_list.append(Tags.objects.create(name= tag))
                # text = "".join(text.split('#'+tag))
            if type == 'save':
                
                user_post = User_Post.objects.create(
                    text=text,
                    user = user,
                    reviewers = 0,
                    likes = 0,
                    name = self.cleaned_data.get('name'),
                    theme = self.cleaned_data.get('theme'),
                    link = self.cleaned_data.get('link'),
                )
                user_post.images.set(images_list)
                user_post.tags.set(tags_list)
                user_post.save()
                # for count in range(132):
                #     print(user_post.name)
            else:
                
                user_post = User_Post.objects.get(
                    pk=type
                )
                # 32454tyth
                print(user_post.text)
                user_post.text = text
                user_post.name = self.cleaned_data.get('name')
                user_post.theme = self.cleaned_data.get('theme')
                user_post.link = self.cleaned_data.get('link')
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