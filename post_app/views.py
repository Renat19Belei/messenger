from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from .forms import messageForm,UserSet, PostForm
from .models import Post, Profile, Tag, Image, Link
from user_app.models import Profile
from chat_app.models import ChatGroup, ChatMessage
from django.http import JsonResponse
from django.urls import reverse_lazy
import json
from django.views.generic.edit import FormView
from  django.contrib.auth.models import User
from  django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.contrib import messages


@login_required(login_url=reverse_lazy('login'))
def MainPageView(request:WSGIRequest):
    """
    Главная страница приложения, где пользователь может создавать посты.
    Если пользователь отправляет форму с изображениями, то создается новый пост.
    """
    profile = Profile.objects.get(user=request.user)
    form1 = messageForm()
    form2 = UserSet()
    if request.method == 'POST':
        if 'images1' in request.POST:
            form1 = messageForm(request.POST)
            if form1.is_valid():
                files = request.FILES.getlist("images")
                remove_List = request.POST.get("images1").split(" ")
                del remove_List[-1]
                remove_List_2 = request.POST.get("images2").split(" ")
                del remove_List_2[-1]
                form1.send(
                    request.user,
                    files,
                    request.POST.get('type'),
                    request.POST.get('imgs'),
                    [remove_List,remove_List_2],
                    request.POST.getlist('tags') + request.POST.getlist('everyTag'),
                    request.POST.getlist('link'),
                    request.POST.get('theme')
                    )
        else:
            form2 = UserSet(request.POST)
            if form2.is_valid():
                form2.save(request.user)
    chatPersonal=ChatGroup.objects.filter(members=profile,is_personal_chat=True)
    messagesList = []
    for chat in chatPersonal:
        messageElem  = ChatMessage.objects.filter(chat_group=chat).order_by('-send_at').first()
        if messageElem:
            messagesList.append(messageElem)
    return render(request,'post_app/main.html',context={
        'form1':form1,
        "form2":form2,
        "messagesList": messagesList
    })



# Декоратор требует авторизации пользователя для доступа к функции
@login_required(login_url=reverse_lazy('login'))
def remove(request:WSGIRequest,pk:int):
    """ 
    Функция для удаления поста по его первичному ключу (id).
    Проверяет, что текущий пользователь является автором поста.
    Если автор совпадает, то пост удаляется, иначе ничего не происходит.
    Возвращает обновленный шаблон с постами или пустой, если все посты удалены.
    """
    # Получаем пост по его первичному ключу (id)
    user_post = get_object_or_404(Post, pk=pk)
    # Проверяем, что автор поста совпадает с текущим пользователем
    if user_post.author == Profile.objects.get(user=request.user):
        # Удаляем пост, если пользователь — автор
        Post.delete(user_post)
    # Возвращаем обновленный шаблон с постами (или пустой, если все удалено)
    return render(request, "post_app/new_posts.html")
@login_required(login_url=reverse_lazy('login'))
def gets(request:WSGIRequest,pk:int):
    """ 
    Функция для получения данных поста по его первичному ключу (id).
    Проверяет, что текущий пользователь является автором поста.
    Если автор совпадает, то собирает данные поста и возвращает их в формате JSON.
    Если автор не совпадает, возвращает ошибку.
    Параметры:
    - request: WSGIRequest — HTTP-запрос от клиента.
    - pk: int — первичный ключ (id) поста, который нужно получить.
    Возвращает:
    - JsonResponse с данными поста, если пользователь является автором.
    - JsonResponse с ошибкой, если пользователь не является автором поста.
    """
    # Получаем пост по id
    user_post = Post.objects.get(pk = int(pk))
    # Проверяем, что текущий пользователь — автор поста
    if user_post.author.user == request.user:
        # Собираем данные поста для передачи на фронт
        text = user_post.content
        topic = user_post.topic
        list_of_imgs = []
        list_of_imgs_pk = []
        for image in user_post.images.all():
            # Добавляем url и pk всех изображений поста
            list_of_imgs += [image.file.url]
            list_of_imgs_pk += [image.pk]
        tags  = []
        for tag in user_post.tags.all():
            tags +=[tag.name]
        links  = []
        for link in Link.objects.filter(post=user_post):
            links.append(link.url)
        # Возвращаем данные поста в формате JSON
        data = JsonResponse({'text':user_post.content,'name':user_post.title,"theme":topic,"link":links,"imgs":list_of_imgs,"imgs_pk":list_of_imgs_pk,"tags":tags,'topic':topic})
        return data
    # Если пользователь не автор поста — возвращаем ошибку
    return JsonResponse({'error':'who are you'})

def like_post(request:WSGIRequest, pk:int):
    """ Функция для обработки запросов на лайк поста.
    Если запрос POST, то добавляет лайк к посту.
    Параметры:
    - request: WSGIRequest — HTTP-запрос от клиента.
    """
    if request.method == "POST":
        post_id = pk
        Cookie = request.COOKIES.get('user_id')
        print(Cookie,1111111111111)
        profile = Profile.objects.get(user=request.user)
        post = get_object_or_404(Post, pk=post_id)
        if (profile in post.likes.all()):
            post.likes.remove(profile)
            post.save()
            return JsonResponse({'likes': post.likes.all().count(),'liked': False})
        else:
            post.likes.add(profile)
            post.save()
            return JsonResponse({'likes': post.likes.all().count(),'liked': True})
    return JsonResponse({'error': 'onlyPost'})

@login_required(login_url=reverse_lazy('login'))
def new_posts(request:WSGIRequest):
    """ Функция для обработки запросов на получение новых постов.
    Если запрос POST, то собирает данные о постах в зависимости от типа запроса.
    Параметры:
    - request: WSGIRequest — HTTP-запрос от клиента.
    Возвращает:
    - JsonResponse с данными постов, если запрос успешен.
    - JsonResponse с ошибкой, если запрос не удался.
    """
    if request.method == "POST":
        list_posts =  [] 
        type = request.POST.get('type')
        profile = Profile.objects.get(user = request.user)
        if type == 'posts':
            all_posts = Post.objects.filter(author = profile)
        elif 'friends' in type:
            # user =  User.objects.get(pk= )
            profileFriend = Profile.objects.get(user_id = int("".join(type.split('friends'))))
            all_posts = Post.objects.filter(author = profileFriend)
        else:
            all_posts = Post.objects.all()
        links = []
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            form = PostForm()
        for post in json.loads(request.POST.get('posts')):
            try:
                
                list_posts.append(all_posts[len(all_posts)-(int(post)-1)]) 
                if list_posts[-1].author != profile:
                    list_posts[-1].views.add(profile)
                    list_posts[-1].save()
                links.append(Link.objects.filter(pk=list_posts[-1].pk)) 
            except Exception as error:
                print(error)
        
        return render(request, "post_app/new_posts.html", context={'list_posts':list_posts, "type":type,'profile':profile})
    return JsonResponse({'error':'onlyPost'})

class Posts(FormView):
    """ Представление для создания и редактирования постов.
    Использует форму messageForm для обработки данных поста.
    При успешной валидации формы вызывается метод form_valid, который обрабатывает
    загруженные изображения, удаляемые изображения и теги, а затем сохраняет пост.
    Параметры:
    - template_name: str — путь к шаблону, который будет использоваться для отображения формы.
    - form_class: type — класс формы, который будет использоваться для обработки данных.
    - success_url: str — URL, на который будет перенаправлен пользователь после успешной отправки формы.
    """
    template_name = "post_app/posts.html"
    form_class = messageForm
    success_url = reverse_lazy('posts')

    # Метод вызывается при успешной валидации формы
    def form_valid(self, form):
        """ Обрабатывает данные формы после успешной валидации.
        Получает загруженные изображения, списки для удаления изображений и теги,
        а затем вызывает метод send формы для сохранения поста.
        Параметры:
        - form: messageForm — форма, содержащая данные поста.
        Возвращает:
        - HttpResponseRedirect — перенаправляет пользователя на success_url после успешной обработки формы
        """
        # Получаем список загруженных изображений
        files = self.request.FILES.getlist("images")
        # Получаем список id изображений для удаления (images1)
        remove_List = self.request.POST.get("images1").split(" ")
        del remove_List[-1]
        # Получаем список id изображений для удаления (images2)
        remove_List_2 = self.request.POST.get("images2").split(" ")
        del remove_List_2[-1]
        # Получаем теги (но не используется напрямую)
        self.request.POST.get('tags')
        # Отправляем данные формы на обработку (создание/редактирование поста)
        form.send(
            self.request.user,
            files,
            self.request.POST.get('type'),  # тип запроса (например, создание или редактирование)
            self.request.POST.get('imgs'),
            [remove_List,remove_List_2],
            self.request.POST.getlist('tags') + self.request.POST.getlist('everyTag'),
            self.request.POST.getlist('link'),
        )
        # Продолжаем стандартную обработку формы
        return super().form_valid(form)