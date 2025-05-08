from .views import *
from django.urls import path

urlpatterns = [
    path('', UserPageView.as_view()),
    path('login/', LoginView.as_view(), name="login")
]