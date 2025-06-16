from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from main_app.forms import messageForm,UserSet,ProfileForm
from .models import Post, Profile, Tag, Image, Link

from django.http import JsonResponse
from django.urls import reverse_lazy
import json
from django.views.generic.edit import FormView
from  django.contrib.auth.models import User
from  django.contrib.auth.decorators import login_required
# Create your views here.
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
    if user_post.author == request.user:
        print("REMOVE")
        Post.delete(user_post)
    return render(request, "post_app/new_posts.html")
def gets(request:WSGIRequest,pk:int):
    # if request.method == 'POST':
    print('heehheeeh',pk)

    user_post= Post.objects.get(pk = pk)
    if user_post.author == request.user:
        text = user_post.content
        list_of_imgs = []
        list_of_imgs_pk = []

        for image in user_post.images.all():
            # Images().image.url
            list_of_imgs += [image.file.url]
            list_of_imgs_pk += [image.pk]
        tags  = []
        for tag in user_post.tags.all():
            tags +=[tag.name]
        data = JsonResponse({'text':text,'name':user_post.title,"theme":user_post,"link":user_post,"imgs":list_of_imgs,"imgs_pk":list_of_imgs_pk,"tags":tags})
        return data
    return 'who are you'
def new_posts(request:WSGIRequest):
    if request.method == "POST":
        list_posts =  [] 
        type = request.POST.get('type')
        
        print(type, 'friends' in type)
        if type == 'posts':
            all_posts = Post.objects.filter(user = request.user)
            # all_posts = User_Post.objects.all()
        if 'friends' in type:
            user = User.objects.get(pk= int("".join(type.split('friends'))))
            all_posts = Post.objects.filter(user = user)
            print(all_posts, user)
        else:
            all_posts = Post.objects.all()
        links = {}
        for post in json.loads(request.POST.get('posts')):
            try:
                
                list_posts.append(all_posts[len(all_posts)-(int(post)-1)]) 
                if list_posts[-1].user != request.user:
                    list_posts[-1].reviewers.add( request.user)
            except Exception as error:
                print(error,12324,5467,89,0,243098765442,3435,677,87654,42)
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
        # remove_dict = 
        remove_List_2 = self.request.POST.get("images2").split(" ")
        del remove_List_2[-1]
        #removing imgs
        self.request.POST.get('tags')
        form.send(
            self.request.user,
            files,
            self.request.POST.get('type'),
            self.request.POST.get('imgs'),
            [remove_List,remove_List_2],
            self.request.POST.getlist('tags'),
            self.request.POST.getlist('link'),
            # self.request.POST.get('title'),
            # self.request.POST.get('content')
            )
            
        return super().form_valid(form)