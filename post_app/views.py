from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from .forms import messageForm,UserSet, PostForm
from .models import Post, Profile, Tag, Image, Link

from django.http import JsonResponse
from django.urls import reverse_lazy
import json
from django.views.generic.edit import FormView
from  django.contrib.auth.models import User
from  django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.contrib import messages


@login_required(login_url=reverse_lazy('login'))
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
                

    return render(request,'post_app/main.html',context={
        'form1':form1,
        "form2":form2
    })
def remove(request:WSGIRequest,pk:int):
    print(request.user)
    user_post = Post.objects.get(pk = pk)
    # print(user_post.user, request.user, 'hehheehehehhe')
    if user_post.author == Profile.objects.get(user=request.user):
        print("REMOVE")
        Post.delete(user_post)
    return render(request, "post_app/new_posts.html")
def gets(request:WSGIRequest,pk:int):
    # if request.method == 'POST':
    print('heehheeeh',pk)

    user_post= Post.objects.get(pk = int(pk))
    print('ok')
    if user_post.author == Profile.objects.get(user=request.user):
        print('okok')
        text = user_post.content
        list_of_imgs = []
        list_of_imgs_pk = []
        print('heh')
        for image in user_post.images.all():
            # Images().image.url
            list_of_imgs += [image.file.url]
            list_of_imgs_pk += [image.pk]
        print('imgs ok')
        tags  = []
        for tag in user_post.tags.all():
            tags +=[tag.name]
        links  = []
        for link in Link.objects.filter(post=user_post):
            links.append(link.url)
        print('t@gs')
        data = JsonResponse({'text':text,'name':user_post.title,"theme":'',"link":links,"imgs":list_of_imgs,"imgs_pk":list_of_imgs_pk,"tags":tags})
        print('WTF')
        return data
    return JsonResponse({'error':'who are you'})
def new_posts(request:WSGIRequest):
    if request.method == "POST":
        list_posts =  [] 
        type = request.POST.get('type')
        
        # print(type, 'friends' in type)
        profile = Profile.objects.get(user = request.user)
        if type == 'posts':
            all_posts = Post.objects.filter(author = profile)
            # all_posts = User_Post.objects.all()
        if 'friends' in type:
            user =  User.objects.get(pk= int("".join(type.split('friends'))))
            profileFriend = Profile.objects.get(user = user)
            all_posts = Post.objects.filter(author = profileFriend)
            print(all_posts, user)
        else:
            all_posts = Post.objects.all()
        
        print(all_posts,31246789032456903241384980)
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
                    list_posts[-1].views.add( profile)
                    print(list_posts[-1].views.all())
                    list_posts[-1].save()
                links.append(Link.objects.filter(pk=list_posts[-1].pk)) 
                # links = 
            except Exception as error:
                print(error,12324,5467,89,0,243098765442,3435,677,87654,42)
        print(all_posts,9999999999999999999999999999999999999999999999999999999999999999)
        
        return render(request, "post_app/new_posts.html", context={'list_posts':list_posts, "type":type})
    return 'onlyPost'

class Posts(FormView):
    template_name = "post_app/posts.html"
    form_class = messageForm
    success_url = reverse_lazy('posts')
    def form_valid(self, form):
        files = self.request.FILES.getlist("images")
        remove_List = self.request.POST.get("images1").split(" ")
        del remove_List[-1]
        # remove_dict = everyTag
        remove_List_2 = self.request.POST.get("images2").split(" ")
        del remove_List_2[-1]
        #removing imgs
        self.request.POST.get('tags')
        print( self.request.POST.getlist('everyTag'),1231212313212313223213, self.request.POST)
        form.send(
            self.request.user,
            files,
            self.request.POST.get('type'),
            self.request.POST.get('imgs'),
            [remove_List,remove_List_2],
            self.request.POST.getlist('tags') + self.request.POST.getlist('everyTag'),
            self.request.POST.getlist('link'),
            # self.request.POST.get('title'),
            # self.request.POST.get('content')
            )
            
        return super().form_valid(form)