from .views import *
from django.urls import path
from . import views

urlpatterns = [
    # path('logout/', LogoutView.as_view(), name = "logout"),
    # path('', views.MainPageView.as_view(), name='main'),
    path('friends/<str:typek>', friends, name='friends'),
    
    
    path('friends_account/<int:pk>',friends_account,name="friends_account"),
    
    # <str:posts>
]