from django.views.generic.edit import FormView
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render,redirect
from .forms import UserForm,AuthenticationForm2
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.core.handlers.wsgi import WSGIRequest
from .models import VerificationCode
from .models import Profile
from .tasks import delete_old_code
from django.utils import timezone
from datetime import timedelta

from django.http import HttpResponse
from django.db.models import Q 
from .forms import AuthenticationForm2
import random
import threading
import qrcode, io 
from PIL import Image
from .forms import AuthenticationForm2 
from django.contrib.auth import login, logout, get_user_model
from .models import Avatar
from post_app.models import Tag, Album
from .forms import ProfileForm, PasswordForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm2(request.POST)

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
                return redirect('main')
            else:
                form.add_error(None, "Невірне ім'я користувача/email або пароль.")

    else:
        form = AuthenticationForm2()

class customLogoutView(LogoutView):
    next_page = "login"

class UserPageView(FormView):
    template_name = "user_app/user.html"
    form_class = UserForm
    success_url = '/user/login/'
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            users = User.objects.filter(username=request.POST.get('username'), is_active=False)
            if len(users):
                users[0].delete()
        return super().dispatch(request, *args, **kwargs)
    def form_invalid(self, form):
        return super().form_invalid(form)
    def form_valid(self, form:AuthenticationForm2):
        user=form.save()
        user.is_active = False
        user.save()
        text_content = random.randint(100000, 999999)
        code= VerificationCode.objects.create(code=str(text_content),username = user.pk)
        self.success_url = f'/user/email/{code.id}'
        profile = Profile.objects.create(user_id=user.pk,date_of_birth=timezone.now().date())
        threading.Thread(target=delete_old_code, args= [code.id]).start()
        send_mail(
            "Subject here",
            str(text_content),
            "illyaepik@gmail.com",
            [form.cleaned_data['username']]
        )
        return super().form_valid(form)

class Get_Random_Qr_Code(View):
    def get(self,request:WSGIRequest):
        buffer = io.BytesIO()
        qrcode.make(
            data=random.Random()
        ).save(buffer, format='PNG') 
        return HttpResponse(buffer.getvalue())

class CustomLoginView(LoginView):
    template_name = "user_app/login.html"
    form_class = AuthenticationForm2

def render_email(request:WSGIRequest, code):
    code= VerificationCode.objects.get(id = code)
    user = User.objects.get(pk=code.username)
    if request.method == 'POST':
        written = ''
        for count in range(6):
            written += request.POST.get(f'code{count+1}')
        if str(code.code) == written:
            user.is_active = True
            user.save()
            VerificationCode.delete(code)
            return redirect("/user/login/")
    return render(request,'user_app/my_email.html',context={'email':user.username})

def albums(request:WSGIRequest):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form_type = request.POST.get("type")
        if form_type == 'album':
            theme=request.POST.get("themeSelect")
            tag=Tag.objects.filter(name=theme).first()
            tag = None
            if not tag:
                tag = Tag.objects.create(name=theme)
            album = Album.objects.create(
                name = request.POST.get("name"),
                topic= tag
            )
        if form_type == 'images':
            album = Album.objects.get(pk=int(request.POST.get("pk")))
            img_list = []
            for img in request.FILES.getlist('images'):
                album.image.add(Image.objects.create(file=img))
                album.save()
            album.save()
    user_albums = Album.objects.all()
    avatars = Avatar.objects.filter(profile=profile,active=False)
    return render(request, 'user_app/albums.html', context= {"albums" :user_albums,'avatars':avatars})

def remove_album_icon(request:WSGIRequest):
    if request.method == 'POST':
        album_id = request.POST.get("album_id")
        album = Album.objects.get(pk=album_id)
        album.icon.delete()
        album.save()
    return redirect('albums')

@login_required
def personal(request:WSGIRequest):
    if not request.user.is_authenticated:
        return redirect('login')

    profile_form = ProfileForm(user=request.user)
    form = PasswordForm()
    profile = Profile.objects.get(user_id = request.user.pk)
    if request.method == 'POST':
        user = request.user
        type = request.POST.get('type')
        if type == 'main_data':
            user.first_name = request.POST.get('first_name')
            user.last_name =request.POST.get('last_name')
            user.email = request.POST.get('email')
            profile.date_of_birth = request.POST.get('date_of_birthday')
            user.save()
        elif type == 'profile':
            avatar=Avatar.objects.filter(profile=profile,shown=True)
            if avatar:
                avatar=avatar.filter(active = True).first()
                avatar.image=request.FILES.get('profile_icon')
                avatar.save()
            else:
                Avatar.objects.create(image=request.FILES.get('profile_icon'), profile = profile)
            for avatar in request.FILES.getlist('avatars'):
                Avatar.objects.create(image=avatar, profile = profile,active=False)
        elif type == 'elec':
            profile.signature = request.FILES.get('elec')
        elif type == 'check_password':
            VerificationCodes = VerificationCode.objects.filter(username=str(user.pk))
            if VerificationCodes:
                for Objectcode in VerificationCodes:
                    VerificationCode.delete(Objectcode)
            password = request.POST.get('password')
            password = request.user.check_password(password)
            code = str(random.randint(100000,999999))
            VerificationCode.objects.create(username=str(user.pk),code = code)
            send_mail(
                "Subject here",
                str(code),
                "illyaepik@gmail.com",
                [request.user.email]
            )
            return JsonResponse({'correct':password})
        elif type == 'check_code':
            verificationCode = VerificationCode.objects.filter(username=str(user.pk)).reverse().first()
            code = str(json.loads(request.POST.get('codes')))
            if verificationCode.code == code:
                for Objectcode in VerificationCode.objects.filter(username=str(user.pk)):
                    VerificationCode.delete(Objectcode)
                return JsonResponse({'correct':True})
            else:
                return JsonResponse({'correct':False})
        elif type == 'edit_password':
            request.user.set_password(request.POST.get('password'))
            request.user.save()
        profile.save()
    return render(request, 'user_app/personal.html',context={
        "form":profile_form,
        'profile':profile,
        "password_form":form
    })