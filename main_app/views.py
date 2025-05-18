from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import  LogoutView
from .forms import messageForm
from .models import *
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
    def form_valid(self, form):
        # instance = form.send(commit=False)
        # instance.user = self.request.user
        # instance.send()
        form.send(self.request.user)
        # print('1233212332132')
        print()
        return super().form_valid(form)
def new_posts(request:WSGIRequest):
    if request.method == "POST":
        try:
            list_posts =  [] 
            print(request.POST)
            for post in json.loads(request.POST.get('posts')):
                print(int(post))
                list_posts.append(User_Post.objects.get(pk=int(post))) 
            print(list_posts)
            return render(request, "main_app/new_posts.html", context={'list_posts':list_posts})
        except Exception as error:

            print(error,12324,5467,89,0,243098765442,3435,677,87654,42)
            return render(request, "main_app/new_posts.html")
    return 'onlyPost'
class CustomLogoutView(LogoutView):
    next_page = "login"

# def get(request):
    # return render(request, 'main_app/main.html')

def personal(request):
    return render(request, 'main_app/personal.html')
class Posts(FormView):
    template_name = "main_app/posts.html"
    form_class = messageForm
    success_url = reverse_lazy('posts')
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs
    def form_valid(self, form):
        # instance = form.send(commit=False)
        # instance.user = self.request.user
        # instance.send()
        form.send(self.request.user)
        # print('1233212332132')
        print()
        return super().form_valid(form)
def posts(request):
    return render(request, 'main_app/posts.html')

def friends(request):
    return render(request, 'main_app/friends.html')

def chats(request):
    return render(request, 'main_app/chat.html')