from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView

from django.contrib.auth.views import  LogoutView
from .models import *

from django.core.handlers.wsgi import WSGIRequest
import json
from django.contrib.auth.decorators import login_required

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LogoutView
from .forms import ProfileForm
from user_app.models import Friendship,Avatar
from post_app.models import Post, Profile, Tag, Image, Link, Album
from chat_app.models import ChatGroup


class CustomLogoutView(LogoutView):
    next_page = "login"

def personal(request:WSGIRequest):
    if not request.user.is_authenticated:

        return redirect('login')
    profile_form = ProfileForm(user=request.user)
    
    profile = Profile.objects.get(user_id = request.user.pk)
    print(profile,'profile')
    if request.method == 'POST':
        print('hello')
        user = request.user
        
        # print
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
        profile.save()
        # if profile_form.is_valid():
        #     profile_form.save(user=request.user)
        # print(profile_form)
    # request.user.password.
    # user = request.user
    return render(request, 'main_app/personal.html',context={
        "form":profile_form,
        'profile':profile

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
            album = Album.objects.create(
                name = request.POST.get("name"),
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
                # print('imgmgg')                # img_list.append(Images.objects.create(image=img))
                album.images.add(Image.objects.create(image=img))
            
            album.save()
        # images 
            # print(album)
            # print(album.images.all())
    user_albums = Album.objects.all()
    avatars = Avatar.objects.filter(profile=profile,active=False)
    print(avatars)
    return render(request, 'main_app/albums.html', context= {"albums" :user_albums,'avatars':avatars})
# =======
#     return render(request, 'main_app/albums.html')

# @login_required 

# >>>>>>> origin/Renat
