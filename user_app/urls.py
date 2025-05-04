from .views import *
from django.urls import path

urlpatterns = [
    path('', UserPageView.as_view())
]