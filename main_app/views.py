from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import  LogoutView
from .forms import messageForm,UserSet
from .models import *
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
import json
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
                form1.send()
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

        for tag in user_post.tags.all():
            text+= '#' + tag.name  + ' '
        data = JsonResponse({'text':text,'name':user_post.name,"theme":user_post.theme,"link":user_post.link,"imgs":list_of_imgs,"imgs_pk":list_of_imgs_pk})
        return data
    return 'who are you'
#     return render(request, "main_app/new_posts.html")
def new_posts(request:WSGIRequest):
    if request.method == "POST":
        list_posts =  [] 
        type = request.POST.get('type')
        if type == 'posts':
            all_posts = User_Post.objects.filter(user = request.user)
            # all_posts = User_Post.objects.all()
        else:
            all_posts = User_Post.objects.all()
        # all_posts=all_posts.reverse()
        # print(all_posts)
        for post in json.loads(request.POST.get('posts')):
            try:
                print(len(all_posts)-(int(post)-1))
                list_posts.append(all_posts[len(all_posts)-(int(post)-1)]) 
            except Exception as error:
                print(error,12324,5467,89,0,243098765442,3435,677,87654,42)
        return render(request, "main_app/new_posts.html", context={'list_posts':list_posts, "type":type})
    return 'onlyPost'


class CustomLogoutView(LogoutView):
    next_page = "login"

# def get(request):
#     return render(request, 'main_app/main.html')

def personal(request):
    return render(request, 'main_app/personal.html')
class Posts(FormView):
    template_name = "main_app/posts.html"
    form_class = messageForm
    success_url = reverse_lazy('posts')
    def form_valid(self, form):
        files = self.request.FILES.getlist("images")
        print(self.request.POST.get("images1"),312,213,312,23,54,67,9,786,5,43,self.request.POST)
        remove_List = self.request.POST.get("images1").split(" ")
        del remove_List[-1]
        # remove_dict = 
        remove_List_2 = self.request.POST.get("images2").split(" ")
        del remove_List_2[-1]
        #removing imgs
        form.send(self.request.user,files,self.request.POST.get('type'),self.request.POST.get('imgs'),[remove_List,remove_List_2])
        return super().form_valid(form)

def friends(request):
    return render(request, 'main_app/friends.html')

def chats(request):
    return render(request, 'main_app/chat.html')