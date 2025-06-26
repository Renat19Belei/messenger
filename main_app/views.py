from django.shortcuts import render, redirect, get_object_or_404

from django.core.mail import send_mail
from django.contrib.auth.views import  LogoutView
from .models import *
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView,DeleteView
# from django.views.generic.detail import 
from django.contrib.auth.views import LogoutView
# from .forms import ProfileForm,PasswordForm 
from user_app.models import Friendship,Avatar,VerificationCode
from post_app.models import Post, Profile, Tag, Image, Link, Album
from chat_app.models import ChatGroup
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import random 
# @login_required
# def change_password(request:WSGIRequest):
#     # request.user.check_password
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user) 
#             return redirect('change_password')
#         else:
#             messages.error(request, 'Будь ласка, виправте помилки нижче.')
#     else:
#         form = PasswordChangeForm(request.user)
class CustomLogoutView(LogoutView):
    next_page = "login"




def friends(request:WSGIRequest,typek='123'):
    user = Profile.objects.get(user = request.user)
    users = Profile.objects.exclude(pk= user.pk)
    requests = []
    recommend = []
    friends_users = []
    for request_user in users:
        friendship = Friendship.objects.filter(profile1=request_user,profile2=user)
        if friendship:
            if friendship.filter(accepted=True):
                friends_users.append(request_user)
            else:
                requests.append(request_user)
        else:
            friendship = Friendship.objects.filter(profile2=request_user,profile1=user)
            if not friendship:
                recommend.append(request_user)
            else:
                if friendship.filter(accepted=True):
                
                    friends_users.append(request_user)
    if request.method == 'POST':
        
        post = json.loads(request.body)
        type_request = post.get("type")
        pk = int(post.get("pk"))
        user_friend = Profile.objects.get(pk = pk)
        name = f"{request.user.pk} {user_friend.user.pk}"
        chat = ChatGroup.objects.filter(name = name)
        if type_request == 'add':
            Friendship.objects.create(
                profile1 = user,
                profile2 = user_friend
            )
        elif type_request == 'confirm':
            if not chat:
                chat_group = ChatGroup.objects.create(name = name,is_personal_chat=True,admin=user)
                chat_group.members.add(user_friend)
                chat_group.members.add(user)
                chat_group.save()
            friend = Friendship.objects.filter(profile2=user,profile1=user_friend,accepted=False).first()
            if friend:
                friend.accepted = True
                friend.save()
        
    return render(request, 'main_app/friends.html', context={
        'typek':typek,
        'requests':requests,
        'friends':friends_users,
        'recommend':recommend
    })
def friends_account(request:WSGIRequest,pk):
    # Получаем пользователя по pk профиля
    user_to_view_profile = Profile.objects.get(pk=pk)
    user_to_view = user_to_view_profile.user
    try:
        # Получаем профиль пользователя (если существует)
        user_to_view_profile = Profile.objects.get(user=user_to_view)
    except Profile.DoesNotExist:
        # Если профиль не найден, выводим имя пользователя в консоль
        print(f"'{user_to_view.username}'")

    # Отправляем данные в шаблон для отображения страницы друга
    return render(request, 'main_app/friends_account.html', context={
        'pk': pk,
        'user': user_to_view,
        'profile': user_to_view_profile
    })