from .views import *
from django.urls import path
from . import views

urlpatterns = [
# leave
    path('chats/', views.chat_view, name='chats'),
    path('leave/<int:pk>', views.leave, name='leave'),
    path('get/', views.get, name='get'),
    # get
]