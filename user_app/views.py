from django.views.generic.edit import FormView
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render,redirect
from .forms import UserForm,AuthenticationForm2
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView 
from django.core.mail import send_mail
from django.core.handlers.wsgi import WSGIRequest
from .models import Code
from .tasks import delete_old_code
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from django.db.models import Q 
from .forms import AuthenticationForm2
# from django.template.loader import render_to_string
# from django.core.mail import send_mail
import random
import threading
import qrcode, io 
from PIL import Image
from .forms import AuthenticationForm2 
from django.contrib.auth import login, logout, get_user_model
# from django.urls import 
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm2(request, data=request.POST) 
        if form.is_valid():
            username_input = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            UserModel = get_user_model()
            user = None

            try:
                user = UserModel.objects.get(Q(username__iexact=username_input) | Q(email__iexact=username_input))
            except UserModel.DoesNotExist:
                user = None
            except UserModel.MultipleObjectsReturned:
                user = None

            if user is not None and user.check_password(password):
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Невірне ім'я користувача/email або пароль.")
    else:
        form = AuthenticationForm2()
    
    return render(request, 'user_app/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login') 


class customLogoutView(DjangoLogoutView):
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
        # user.email = user.username
        user.save()
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
    


class LoginView(DjangoLoginView):
    template_name = "user_app/login.html"
    form_class = AuthenticationForm2

    def post(self, request, *args, **kwargs): # <<<--- ЭТОТ МЕТОД ДОЛЖЕН БЫТЬ ВНУТРИ КЛАССА
        form = self.get_form()
        if form.is_valid():
            username_input = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            UserModel = get_user_model()
            user = None

            try:
                user = UserModel.objects.get(Q(username__iexact=username_input) | Q(email__iexact=username_input))
            except UserModel.DoesNotExist:
                user = None
            except UserModel.MultipleObjectsReturned:
                user = None 

            if user is not None and user.check_password(password):
                login(request, user)
                return self.form_valid(form) 
            else:
                form.add_error(None, "Невірне ім'я користувача/email або пароль.")
                return self.form_invalid(form) 
        else:
            return self.form_invalid(form) 
    # def form_valid(self, form):
        
    #     print(self.request.current_user.email)
def authorization(request:WSGIRequest):
        error = ""
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username= username, password = password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                error = "Username or password is not correct"
        
        return render(request,template_name= "user/authorization.html", context={"error": error})

def render_email(request:WSGIRequest, code):
    # print(type(request))
    print()
    code= Code.objects.get(id = code)
    if request.method == 'POST':
        # print('eeeeee', type(code.code),type(request.POST.get('code')))
        written = ''
        for count in range(6):
            written += request.POST.get(f'code{count+1}')
        if str(code.code) == written:
            print('wrerwewer')
            code.user_id.is_active = True
            code.user_id.save()
            Code.delete(code)
            return redirect("/user/login/")


    return render(request,'user_app/my_email.html',context={'email':code.user_id.email})