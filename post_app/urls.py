from .views import *
from django.urls import path
from . import views

urlpatterns = [
    path('remove/<int:pk>', remove, name='remove'),
    path('get/<int:pk>', gets, name='get'),
    path('list_posts/', new_posts, name= 'list'),
    path('posts/', Posts.as_view(), name='posts'),
]