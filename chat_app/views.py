from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.models import User
from main_app.models import Profile
# Create your views here.
# def chats(request:WSGIRequest):
#     return render(request, 'main_app/chat.html')
def chat_view(request:WSGIRequest):
    profile = Profile.objects.get(user=request.user)
    users_queryset = User.objects.filter(is_active=True).exclude(pk=request.user.pk)
    users = []
    profiles = Profile.objects.filter(friends=profile)
    print(profiles)
    # profiles = profiles.filter(user=users_queryset)
    # for user in users_queryset:
        # if profile in Profile.objects.get(user=).friends:
            # pass
    # friends=request.user
    context = {
        'contacts': profiles, 
    }
    return render(request, 'chat_app/chat.html', context)