from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import  LogoutView
# Create your views here.
class MainPageView(TemplateView):
    template_name = "main_app/main.html"
class CustomLogoutView(LogoutView):
    next_page = "login"