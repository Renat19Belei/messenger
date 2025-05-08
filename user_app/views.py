from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth.views import LoginView
# Create your views here.

class UserPageView(FormView):
    template_name = "user_app/user.html"
    form_class = UserForm
    success_url = '/'
    def form_valid(self, form):
        # user  = User(
        #     username = form.username,
        #     email = UserForm(form).email
        # )
        # print(self.cleaned_data)
        form.save()
        return super().form_valid(form)

class LoginView(LoginView):
    template_name = "user_app/login.html"