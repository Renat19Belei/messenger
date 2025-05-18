from .views import *
from django.urls import path
# from . import views

urlpatterns = [
    # path('logout/', LogoutView.as_view(), name = "logout"),
    # path('', views.MainPageView.as_view(), name='main'),
    path('personal/', personal, name='personal'),
    path('posts/', posts, name='posts'),
    path('friends/', friends, name='friends'),
    path('chats/', chats, name='chats'),
    path('list_posts/', new_posts, name= 'list')
    # <str:posts>
]