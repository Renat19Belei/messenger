from .views import *
from django.urls import path

urlpatterns = [
    path('logout/', LogoutView.as_view(), name = "logout")
]