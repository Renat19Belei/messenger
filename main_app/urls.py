from .views import *
from django.urls import path
from . import views

urlpatterns = [
    path('logout/', LogoutView.as_view(), name = "logout"),
    path('', views.main, name='main'),
    path('personal/', views.personal, name='personal'),
    path('posts/', views.posts, name='posts'),
    path('friends/', views.friends, name='friends'),
    path('chats/', views.chats, name='chats'),
]