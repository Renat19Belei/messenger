from django import forms
from .models import *
from django.contrib.auth.models import User
import json
STANDARD_TAG_NAMES = [
    "відпочинок", "натхнення", "життя", "природа", "читання",
    "спокій", "гармонія", "музика", "фільми", "подорожі"
]

class PostForm(forms.ModelForm):
    
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(name__in=STANDARD_TAG_NAMES).order_by("name"),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Post  
        fields = ['title', 'content', 'tags', 'images']
class messageForm(forms.Form):
    # Форма для создания и редактирования поста

    # Название публикации
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Напишіть назву публікації","class": "FormInput nameInput"}),
        label='Назва публікації',
        max_length=255
    )
    # Тема публикации
    theme = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Напишіть тему публікаціїї","class": "FormInput themeInput"}),
        label='Тема публікації',
        max_length=255
    )
    # Текст публикации
    text = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Напишіть текст публікації","class": "BigFormInput textInput"}),
        label='',
        max_length=2000
    )

    # Метод для сохранения или редактирования поста
    def send(self, user, images, type='save', imgs=[], remove_List=[[],[]], tags=[], links=[],theme=''):
        """
        Метод для создания или редактирования поста.

        user: текущий пользователь (автор поста)
        images: список новых загруженных файлов (картинок)
        type: 'save' для создания нового поста, иначе — id редактируемого поста
        imgs: список id уже существующих изображений (pk)
        remove_List: список списков с индексами удаляемых изображений (0 — новые, 1 — существующие)
        tags: список тегов (строки с #)
        links: список ссылок для поста
        """
        if user and user.is_authenticated:
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
            if type == 'save':
                
                user_post = Post.objects.create(
                    author = Profile.objects.get(user = user),
                    title = self.cleaned_data.get('name'),
                    content = self.cleaned_data.get('text'),
                    topic = theme
                )
                user_post.images.set(images_list)
                user_post.tags.set(tags_list)
                user_post.save()
            else:
                
                user_post = Post.objects.get(
                    pk=type
                )
                if user_post.author.user == user:
                    user_post.content = text
                    user_post.content = theme
                    user_post.title = self.cleaned_data.get('name')
                    user_post.images.set(images_list)
                    user_post.tags.set(tags_list)
                    user_post.save()
            link_list = []
            for link in links:
                link_list += [Link.objects.create(url=link, post = user_post)]
class UserSet(forms.Form):
    # Форма для редактирования данных пользователя
    # Поля формы для ввода данных пользователя
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Введіть Ваше ім’я","class": "FormInput firstNameInput"}),label='Ім’я',max_length=255)
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Введіть Ваше прізвище","class": "FormInput lastNameInput"}),label='Прізвище',max_length=255)
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "@","class": "FormInput lastNameInput"}),label='Ім’я користувача',max_length=255)  
    def save(self,user):
        user.email = user.username
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username = self.cleaned_data.get('username')
        user.save()