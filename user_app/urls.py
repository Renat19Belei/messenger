from .views import *
from django.urls import path

urlpatterns = [
    path('', UserPageView.as_view(), name='user'),
    path('login/', LoginView.as_view(), name="login"),
    path('email/<code>', render_email, name="login"),
    path('logout/', LogoutView.as_view(), name = "logout")
]