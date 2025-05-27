from .views import *
from django.urls import path
# from . import views

urlpatterns = [
    # path('logout/', LogoutView.as_view(), name = "logout"),
    # path('', views.MainPageView.as_view(), name='main'),
    path('personal/', personal, name='personal'),
    path('posts/', Posts.as_view(), name='posts'),
    path('friends/', friends, name='friends'),
    path('chats/', chats, name='chats'),
    path('remove/<int:pk>', remove, name='remove'),
    path('get/<int:pk>', gets, name='get'),
    path('list_posts/', new_posts, name= 'list'),
    path('friends_account/<int:pk>',friends_account,name="friends_account")
    # <str:posts>
]