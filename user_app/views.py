from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.core.mail import send_mail
import random
# from django.urls import 
# Create your views here.

class UserPageView(FormView):
    template_name = "user_app/user.html"
    form_class = UserForm
    success_url = '/user/login/'
    def form_valid(self, form):
        
        # First, render the plain text content.
        text_content = random.randint(10000, 99999)
        # Secondly, render the HTML content.
        # html_content = render_to_string(
        #     "user_templates/user_app/my_email.html",
        #     context={"my_variable": 42},
        # )

        # Then, create a multipart email instance.
        print(form.cleaned_data['email'])
        send_mail(
            "Subject here",
            str(text_content),
            "illyaepik@gmail.com",
            [form.cleaned_data['email']]
        )

        # Lastly, attach the HTML content to the email instance and send.
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()
        # user  = User(
        #     username = form.username,
        #     email = UserForm(form).email
        # )
        # print(self.cleaned_data)
        form.save()
        return super().form_valid(form)

class LoginView(LoginView):
    template_name = "user_app/login.html"
    # def form_valid(self, form):
    #     print(self.request.current_user.email)
        

# def render(self, form):