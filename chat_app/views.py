from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.contrib.auth.models import User
from user_app.models import Profile,Friendship
from .models import ChatMessage,ChatGroup
# Create your views here.
# def chats(request:WSGIRequest):
#     return render(request, 'main_app/chat.html')
def chat_view(request:WSGIRequest):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.POST.get('type')=='personal':
            # pk = 
            friend_profile = Profile.objects.filter(user_id=int(request.POST.get('pk')))
            print(friend_profile,profile)
            group = ChatGroup.objects.filter(members=friend_profile[0]).filter(members=profile).first()
            print('7564324i56mlbutvjompuithk')
            # friendship = Friendship.objects.filter(profile1=profile,profile2 = friend_profile,accepted=True)
            # if not len(profiles):
            #     friendship = Friendship.objects.filter(profile2=profile,profile1 = friend_profile,accepted=True)
            messages = ChatMessage.objects.filter(chat_group=group.pk)
            messages_list = []
            for message in messages:
                messages_list.append({
                    'message':message.content,
                    # "avatar":message.author 
                    # 'send_at':message.send_at
                })
                # print(message.content,message.send_at)
            # return render(request, 'chat_app/message.html', {
            #     'messages':messages,
            #     'pk':group.pk
            # })
            return JsonResponse({   
                'pk':group.pk,
                'messages':messages_list
            })
    # users_queryset = User.objects.filter(is_active=True).exclude(pk=request.user.pk)
    # users = []
    
    # profiles = Profile.objects.filter(friends=profile)
    # profiles = Profile.objects.all()
    profiles = []
    
    for friendship in Friendship.objects.filter(profile1 = profile,accepted=True):
        profiles.append(friendship.profile2)
    for friendship in Friendship.objects.filter(profile2 = profile,accepted=True):
        profiles.append(friendship.profile1)
    # print(profiles)
    # profiles = profiles.filter(user=users_queryset)
    # for user in users_queryset:
        # if profile in Profile.objects.get(user=).friends:
            # pass
    # friends=request.user
    context = {
        'contacts': profiles, 
    }
    return render(request, 'chat_app/chat.html', context)