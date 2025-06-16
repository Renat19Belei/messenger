from django import forms
from .models import *
from django.contrib.auth.models import User
import re,json
# User = get_user_model()
class messageForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Напишіть назву публікації","class": "FormInput nameInput"}),label='Назва публікації',max_length=255)
    theme = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Напишіть тему публікаціїї","class": "FormInput themeInput"}),label='Тема публікації',max_length=255, required=False)

    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Напишіть текст публікації","class": "BigFormInput textInput"}),label='',max_length=2000)

    #     
    def send(self, user, images,type = 'save',imgs=[],remove_List=[[],[]],tags=[],links = []):
        print(user)
        if user and user.is_authenticated:
            # Image
            images_list = []
            tags_list = []
            try:
                count = 0
                for img in json.loads(imgs):
                    if not (str(count) in remove_List[1]):
                        images_list += [Image.objects.get(pk=int(img))]
                    count+= 1
                
            except Exception as error:
                print(error)
            try:
                count =0
                for image in images:
                    print('1345678909-=0-9876543212324567890-',image)
                    if not (str(count) in remove_List[0]):
                        images_list += [Image.objects.create(file=image,filename='lol')]
                    count+=1
            except Exception as error:
                print(error)
            text = self.cleaned_data.get('text')
            for tag in tags:
                tag = tag[1::]
                if Tag.objects.filter(name = tag):
                    tags_list.append(Tag.objects.filter(name = tag).first())
                else:
                    tags_list.append(Tag.objects.create(name= tag))
            
                # text = "".join(text.split('#'+tag))
            if type == 'save':
                
                user_post = Post.objects.create(
                    # text=text,
                    author = Profile.objects.get(user = user),
                    # reviewers = 0,
                    
                    # name = self.cleaned_data.get('name'),
                    # theme = self.cleaned_data.get('theme'),
                    # link = self.cleaned_data.get('link'),
                    title = self.cleaned_data.get('name'),
                    content = self.cleaned_data.get('text'),
                )
                user_post.images.set(images_list)
                user_post.tags.set(tags_list)
                # user_post.links.set(link_list)
                
                user_post.save()
                # for link in links:
                #     lonk = Link.objects.create(url=link,post=user_post)
                    

                # for count in range(132):
                #     print(user_post.name)
            else:
                
                user_post = Post.objects.get(
                    pk=type
                )
                if user_post.author.user == user:
                    user_post.content = text
                    user_post.title = self.cleaned_data.get('name')
                    # user_post.theme = self.cleaned_data.get('theme')
                    # user_post.link = self.cleaned_data.get('link')
                    user_post.images.set(images_list)
                    user_post.tags.set(tags_list)
                    user_post.save()
            link_list = []
            for link in links:
                link_list += [Link.objects.create(url=link, post = user_post)]
        print('heehehewqsxcvbnm')
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