from django.views.generic.edit import FormView
from django.views.generic import View

from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render,redirect
from .forms import UserForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.core.handlers.wsgi import WSGIRequest
from .models import Code
from .tasks import delete_old_code
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
# from django.template.loader import render_to_string
# from django.core.mail import send_mail
import random
import threading
import qrcode, io 
from PIL import Image
# from django.urls import 
# Create your views here.
class customLogoutView(LogoutView):
    # success_url = '/user/login/'
    next_page = "login"

class UserPageView(FormView):
    template_name = "user_app/user.html"
    form_class = UserForm
    success_url = '/user/login/'
    def form_valid(self, form):
        
        # First, render the plain text content.
        user=form.save()
        user.is_active = False
        user.email = user.username
        text_content = random.randint(100000, 999999)
        code= Code.objects.create(code=text_content,user_id = user)
        self.success_url = f'/user/email/{code.id}'
        # delete_old_code.apply_async(
            # args=[code.id],
            # eta=timezone.now() + timedelta(hours=1)
        # )
        threading.Thread(target=delete_old_code, args= [code.id]).start()
        # Secondly, render the HTML content.
        # html_content = render_to_string(
        #     "user_templates/user_app/my_email.html",
        #     context={"my_variable": 42},
        # )

        # Then, create a multipart email instance.
        # print(form.cleaned_data['email'])
        send_mail(
            "Subject here",
            str(text_content),
            "illyaepik@gmail.com",
            [form.cleaned_data['username']]
        )

        # Lastly, attach the HTML content to the email instance and send.
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()
        # user  = User(
        #     username = form.username,
        #     email = UserForm(form).email
        # )
        # print(self.cleaned_data)
        
        return super().form_valid(form)
    # def get_context_data(self, **kwargs):
    #     return super().get_context_data(**kwargs)



class Get_Random_Qr_Code(View):

    def get(self,request:WSGIRequest):
        
        buffer = io.BytesIO()
        qrcode.make(
            data=random.Random()
        ).save(buffer, format='PNG') 
        return HttpResponse(buffer.getvalue())
    


class LoginView(LoginView):
    template_name = "user_app/login.html"
    # def form_valid(self, form):
        
    #     print(self.request.current_user.email)


def render_email(request:WSGIRequest, code):
    # print(type(request))
    code= Code.objects.get(id = code)
    if request.method == 'POST':
        # print('eeeeee', type(code.code),type(request.POST.get('code')))
        written = ''
        for count in range(6):
            written += request.POST.get(f'code{count+1}')
        if str(code.code) == written:
            print('wrerwewer')
            code.user_id.is_active = True
            return redirect("/user/login/")


    return render(request,'user_app/my_email.html')