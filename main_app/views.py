from django.shortcuts import render, redirect, get_object_or_404


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
from .forms import ProfileForm,PasswordForm
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

@login_required
def personal(request:WSGIRequest):
    if not request.user.is_authenticated:

        return redirect('login')

    profile_form = ProfileForm(user=request.user)
    form = PasswordForm()
    profile = Profile.objects.get(user_id = request.user.pk)
    print(profile,'profile')
    if request.method == 'POST':
        # form = PasswordForm(request.POST)
        # if form.is_valid():
        #     user = form.save()
        #     update_session_auth_hash(request, user) 
        #     return redirect('change_password')
        # else:
        #     messages.error(request, 'Будь ласка, виправте помилки нижче.')
        # print('hello')
        user = request.user
        
        # print
        # check_password
        type = request.POST.get('type')
        if type == 'main_data':
            user.first_name = request.POST.get('first_name')
            user.last_name =request.POST.get('last_name')
            user.email = request.POST.get('email')
            profile.date_of_birth = request.POST.get('date_of_birthday')
            user.save()
            # profile
            # elec
        elif type == 'profile':
            avatar=Avatar.objects.filter(profile=profile,shown=True)
            if avatar:
                avatar=avatar.filter(active = True).first()
                avatar.image=request.FILES.get('profile_icon')
                # avatars
                avatar.save()
            else:
                # 
                Avatar.objects.create(image=request.FILES.get('profile_icon'), profile = profile)
            for avatar in request.FILES.getlist('avatars'):
                print(avatar)
                Avatar.objects.create(image=avatar, profile = profile,active=False)
            # profile.icon = 
        elif type == 'elec':

            profile.signature = request.FILES.get('elec')
            print(profile.signature,8976543213)
        elif type == 'check_password':
            password = request.POST.get('password')
            password = request.user.check_password(password)
            VerificationCode.objects.create(username=str(user.pk),code = random.randint(100000,999999))
            return JsonResponse({'correct':password})
        elif type == 'check_code':
            verificationCode = VerificationCode.objects.filter(username=str(user.pk)).first()
            
        profile.save()
        # JsonResponse
        # if profile_form.is_valid():
        #     profile_form.save(user=request.user)
        # print(profile_form)
    # request.user.password.
    # user = request.user
    
    return render(request, 'main_app/personal.html',context={
        "form":profile_form,
        'profile':profile,
        "password_form":form
        # 'profile_icon':profile.icon
        # 'first_name':user.first_name,
        # 'last_name':user.last_name,
        # 'email':user.email,
        # 'password':user.password,
    })


def friends(request:WSGIRequest,typek='123'):
    user = Profile.objects.get(user = request.user)
    users = Profile.objects.exclude(pk= user.pk)
    # ,friends=request.user.pk
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
                # else:
                #     requests.append(request_user)
        # if notProfile.objects.filter(user = request_user):
        #     friends_users.append(request_user)
        # else:
        #     requests.append(request_user)
    if request.method == 'POST':
        
        post = json.loads(request.body)
        # confirm
        type_request = post.get("type")
        print(type_request)
        pk = post.get("pk")
        user_friend = Profile.objects.get(user_id = pk)
        name = f"{request.user.pk} {user_friend.user.pk}"
        chat = ChatGroup.objects.filter(name = name)

        
            # print(name)
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
        # user_friend.friends.add(user)
        # user_friend.save()
        
    print(requests,friends_users)
    return render(request, 'main_app/friends.html', context={
        'typek':typek,
        'requests':requests,
        'friends':friends_users,
        'recommend':recommend
    })
def friends_account(request:WSGIRequest,pk):
    user_to_view = get_object_or_404(User, pk=pk)
    # albums_for_friend = Album.objects.filter(user=user_to_view).order_by('-year', 'name') 
    user_to_view_profile = None
    try:
        user_to_view_profile = Profile.objects.get(user=user_to_view)
    except Profile.DoesNotExist:
        print(f"'{user_to_view.username}'")


    return render(request, 'main_app/friends_account.html', context={
        'pk': pk,
        'user': user_to_view,
        'profile': user_to_view_profile, 
        # 'albums': albums_for_friend,
    })


def albums(request:WSGIRequest):
# <<<<<<< HEAD
    # profile  = Profile.objects.get(user=request.user)
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
                # created_at = request.POST.get("created_at"),
                # priview_image = request.POST.get("priview_image"),
                # image = request.POST.get("image"),
                # shown = request.POST.get("shown"),
                # topic = request.POST.get("topic"),
                
            )
        if form_type == 'images':
            # print('tyuyiuopiuytwefsvbgnyujk7iy6trewqergtyu798')
            album = Album.objects.get(pk=int(request.POST.get("pk")))
            img_list = []
            print(request.FILES)
            for img in request.FILES.getlist('images'):
                print('imgmgg',img)            
                album.image.add(Image.objects.create(file=img))
                album.save()
            album.save()
        # images 
            # print(album)
            # print(album.images.all())
    user_albums = Album.objects.all()
    avatars = Avatar.objects.filter(profile=profile,active=False)
    print(avatars)
    return render(request, 'main_app/albums.html', context= {"albums" :user_albums,'avatars':avatars})
def remove_album_icon(request:WSGIRequest):
    pass
#             print(album)
#             print(album.images.all())
#     user_albums = Album.objects.filter(user=request.user)
    
#     return render(request, 'main_app/albums.html', context= {"albums" :user_albums})
# def album_detail_view(request, album_pk):
#     album = get_object_or_404(Album, pk=album_pk)
#     all_images = list(album.images.all().order_by('id')) 
#     split_point = (len(all_images) + 1) // 2
#     row1_images = all_images[:split_point]
#     row2_images = all_images[split_point:]

#     context = {
#         'album': album,
#         'row1_images': row1_images,
#         'row2_images': row2_images,
#     }
#     return render(request, 'main_app/albums.html', context)
