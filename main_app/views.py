from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import  LogoutView
# Create your views here.
class MainPageView(TemplateView):
    template_name = "main_app/main.html"
class CustomLogoutView(LogoutView):
    next_page = "login"

def main(request):
    return render(request, 'main_app/main.html')

def personal(request):
    return render(request, 'main_app/personal.html')

def posts(request):
    return render(request, 'main_app/posts.html')

def friends(request):
    return render(request, 'main_app/friends.html')

def chats(request):
    return render(request, 'main_app/chat.html')