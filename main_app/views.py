from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import  LogoutView
from .forms import messageForm
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
    # def form_valid(self, form):
    #     instance = form.send(commit=False)
    #     instance.user = self.request.user
    #     instance.send()
    #     # form.send()
    #     print('1233212332132')
    #     return super().form_valid(form)
class CustomLogoutView(LogoutView):
    next_page = "login"

# def get(request):
    # return render(request, 'main_app/main.html')

def personal(request):
    return render(request, 'main_app/personal.html')

def posts(request):
    return render(request, 'main_app/posts.html')

def friends(request):
    return render(request, 'main_app/friends.html')

def chats(request):
    return render(request, 'main_app/chat.html')