from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.contrib.auth.models import User
from user_app.models import Profile,Friendship
from .models import ChatMessage,ChatGroup

def leave(request:WSGIRequest,pk:int):
    profile = Profile.objects.get(user=request.user)
    chat_group = ChatGroup.objects.filter(pk=int(pk)).filter(members=profile).first()
    if chat_group.admin == profile:
        chat_group.delete()
    else:
        chat_group.members.remove(profile)
    return JsonResponse({'heh':'heh'})
def get(request:WSGIRequest):
    profile = Profile.objects.get(user=request.user)
    chat_group = ChatGroup.objects.filter(pk=int(request.POST.get('pk'))).filter(members=profile).first()
    name = chat_group.name

    members = chat_group.members.all()
    members_list = {}
    for member in members:
        members_list[str(member.pk)] = '312132'
    avatar=None
    if chat_group.avatar:
        avatar=chat_group.avatar.url
    return JsonResponse({
        'name':name,
        'members':members_list,
        'avatar':avatar
    })
def chat_view(request:WSGIRequest):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.POST.get('type')=='groupCreation' or request.POST.get('type')=='groupEdit':
            if request.POST.get('type')=='groupCreation':
                chatGroup =ChatGroup.objects.create(
                    admin=profile,
                    name = request.POST.get('name'),
                    avatar=request.FILES.get('group_img')
                )
            else:
                chatGroup =ChatGroup.objects.get(pk=int(request.POST.get('pk')))
                chatGroup.name = request.POST.get('name')
                chatGroup.avatar=request.FILES.get('group_img')
                chatGroup.members.clear()
            chatGroup.members.add(profile)
            for pk in request.POST.getlist('members'):
                chatGroup.members.add(Profile.objects.filter(pk=int(pk)).first())
            
            chatGroup.save()
        if request.POST.get('type')=='personal':
            friend_profile = Profile.objects.filter(pk=int(request.POST.get('pk')))
            group = ChatGroup.objects.filter(members=friend_profile[0],is_personal_chat=True).filter(members=profile).first()
            messages = ChatMessage.objects.filter(chat_group=group.pk).order_by('-send_at')
            messages_list = []
            for message in messages:
                messages_list.append({
                    'message':message.content,
                })
            
            return render(request, 'chat_app/message.html', {
                'messages':messages,
                'pk':group.pk
            })
        if  request.POST.get('type')=='group':
            chat_group = ChatGroup.objects.filter(pk=int(request.POST.get('pk'))).filter(members=profile).first()
            messages = ChatMessage.objects.filter(chat_group=chat_group).order_by('-send_at')
            is_admin = chat_group.admin == profile
            messages_list = []
            for message in messages:
                messages_list.append({
                    'message':message.content,
                })
            
            return render(request, 'chat_app/message.html', {
                'messages':messages,
                'pk':int(request.POST.get('pk')),
                'is_admin':int(is_admin)
            })
    profiles = []
    
    for friendship in Friendship.objects.filter(profile1 = profile,accepted=True):
        profiles.append(friendship.profile2)
    for friendship in Friendship.objects.filter(profile2 = profile,accepted=True):
        profiles.append(friendship.profile1)
    chatGroups=ChatGroup.objects.filter(members=profile,is_personal_chat=False)
    chatPersonal=ChatGroup.objects.filter(members=profile,is_personal_chat=True)
    messagesList = []
    for chat in chatPersonal:
        messageElem  = ChatMessage.objects.filter(chat_group=chat).order_by('-send_at').first()
        if messageElem:
            messagesList.append(messageElem)
        
    context = {
        'contacts': profiles, 
        'chatGroups':chatGroups,
        'messagesList':messagesList
    }
    return render(request, 'chat_app/chat.html', context)