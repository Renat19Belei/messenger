from .views import *
from django.urls import path
from . import views

urlpatterns = [

    path('chats/', views.chat_view, name='chats'),
]