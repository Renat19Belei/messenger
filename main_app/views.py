from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import  LogoutView
from .forms import messageForm,UserSet,ProfileForm,AlbumForm
from .models import *
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
import json
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# Create your views here.
class MainPageView(FormView):
    template_name = "main_app/main.html"
    form_class = messageForm
    success_url = reverse_lazy('main')
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Instantiate forms for GET request (initial display)
        context['form1'] = messageForm()
        context['form2'] = UserSet()
        return context
    def post(self, request, *args, **kwargs):
        form1 = messageForm(request.POST, prefix='form1')
        form2 = UserSet(request.POST, prefix='form2')
        print('heheeheh')
        if 'images1' in request.POST:
            if form1.is_valid():
                return self.form_valid(form1)
            else:
                return self.form_invalid(form1)
        else:
            print('hello')
            if form2.is_valid():
                return self.form_valid(form2)
            else:
                return self.form_invalid(form2)
    def form_valid(self, form):
        print('heelo')
        if self.request.POST.get('formType') == 'modalForm':
            form.send(self.request.user,self.request.FILES.getlist("images"),self.request.POST.get('type'),self.request.POST.get('imgs'))
        else:
            print(form,self.request.user)
            form.save(self.request.user)
        return super().form_valid(form)
def MainPageView(request:WSGIRequest):
    form1 = messageForm()
    form2 = UserSet()
    if request.method == 'POST':
        if 'images1' in request.POST:
            form1 = messageForm(request.POST)
            if form1.is_valid():
                print(request.POST.getlist('tags'),'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
                form1.send(request.user,request.FILES.getlist('images'),request.POST.get('type'),request.POST.get('imgs'),request.POST.getlist('tags'),request.POST.getlist('link'))
        else:
            form2 = UserSet(request.POST)
            if form2.is_valid():
                form2.save(request.user)
                

    return render(request,'main_app/main.html',context={
        'form1':form1,
        "form2":form2
    })
def remove(request:WSGIRequest,pk:int):
    print(request.user)
    user_post = User_Post.objects.get(pk = pk)
    # print(user_post.user, request.user, 'hehheehehehhe')
    if user_post.user == request.user:
        print("REMOVE")
        User_Post.delete(user_post)
    return render(request, "main_app/new_posts.html")
def gets(request:WSGIRequest,pk:int):
    # if request.method == 'POST':
    print('heehheeeh',pk)

    user_post= User_Post.objects.get(pk = pk)
    if user_post.user == request.user:
        text = user_post.text
        list_of_imgs = []
        list_of_imgs_pk = []

        for image in user_post.images.all():
            # Images().image.url
            list_of_imgs += [image.image.url]
            list_of_imgs_pk += [image.pk]
        tags  = []
        for tag in user_post.tags.all():
            tags +=[tag.name]
        data = JsonResponse({'text':text,'name':user_post.name,"theme":user_post.theme,"link":user_post.link,"imgs":list_of_imgs,"imgs_pk":list_of_imgs_pk,"tags":tags})
        return data
    return 'who are you'
#     return render(request, "main_app/new_posts.html")
def new_posts(request:WSGIRequest):
    if request.method == "POST":
        list_posts =  [] 
        type = request.POST.get('type')
        
        print(type, 'friends' in type)
        if type == 'posts':
            all_posts = User_Post.objects.filter(user = request.user)
            # all_posts = User_Post.objects.all()
        if 'friends' in type:
            print(int("".join(type.split('friends'))),'qweewq')
            user = User.objects.get(pk= int("".join(type.split('friends'))))
            all_posts = User_Post.objects.filter(user = user)
            print(all_posts, user)
        else:
            all_posts = User_Post.objects.all()
        links = {}
        # for post in all_posts:
        #     links2 = Link.objects.filter(post = post)
        #     links[post.pk] = links2
        # all_posts=all_posts.reverse()
        # print(all_posts)
        for post in json.loads(request.POST.get('posts')):
            try:
                print(len(all_posts)-(int(post)),'423567890-9')
                list_posts.append(all_posts[len(all_posts)-(int(post)-1)]) 
            except Exception as error:
                print(error,12324,5467,89,0,243098765442,3435,677,87654,42)
        return render(request, "main_app/new_posts.html", context={'list_posts':list_posts, "type":type})
    return 'onlyPost'


class CustomLogoutView(LogoutView):
    next_page = "login"

# def get(request):
#     return render(request, 'main_app/main.html')
def personal(request:WSGIRequest):
    print(request.user,request.user.is_authenticated)
    if not request.user.is_authenticated:

        return redirect('login')
    profile_form = ProfileForm(user=request.user)
    
    profile = Profile.objects.get(user_id = request.user.pk)
    print(profile,'profile')
    if request.method == 'POST':
        print('hello')
        user = request.user
        # profile_form = ProfileForm(request.POST,user=request.user)
        user.first_name = request.POST.get('first_name')
        user.last_name =request.POST.get('last_name')
        user.email = request.POST.get('email')
        print(request.POST.get('date_of_birthday'))
        
        print(request.POST)
        profile.birthday = request.POST.get('date_of_birthday')
        print(profile.birthday)
        profile.save()
        user.save()
        # if profile_form.is_valid():
        #     profile_form.save(user=request.user)
        # print(profile_form)
    # request.user.password.
    # user = request.user
    return render(request, 'main_app/personal.html',context={
        "form":profile_form
        # 'first_name':user.first_name,
        # 'last_name':user.last_name,
        # 'email':user.email,
        # 'password':user.password,
    })
class Posts(FormView):
    template_name = "main_app/posts.html"
    form_class = messageForm
    success_url = reverse_lazy('posts')
    def form_valid(self, form):
        files = self.request.FILES.getlist("images")
        remove_List = self.request.POST.get("images1").split(" ")
        del remove_List[-1]
        # remove_dict = 
        remove_List_2 = self.request.POST.get("images2").split(" ")
        del remove_List_2[-1]
        #removing imgs
        self.request.POST.get('tags')
        form.send(
            self.request.user,
            files,self.request.POST.get('type'),
            self.request.POST.get('imgs'),
            [remove_List,remove_List_2],
            self.request.POST.getlist('tags'),
            self.request.POST.getlist('link'))
        return super().form_valid(form)

def friends(request,typek='123'):
    return render(request, 'main_app/friends.html', context={'typek':typek})
def friends_account(request,pk):
    user =User.objects.get(pk = pk)
    return render(request, 'main_app/friends_account.html',context={'pk':pk,'user':user})
def chats(request):
    return render(request, 'main_app/chat.html')
def albums(request):
    profile  = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        album = Album.objects.create(
            name = request.POST.get("name"),
            year = request.POST.get("year"),
            theme = request.POST.get("theme"),
            user = profile
        )
    return render(request, 'main_app/albums.html')