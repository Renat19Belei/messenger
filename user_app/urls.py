from .views import *
from django.urls import path

urlpatterns = [
    path('', UserPageView.as_view(), name='user'),
    path('login/', user_login, name="login"),
    path('img/', Get_Random_Qr_Code.as_view(), name="img"),
    path('email/<code>', render_email, name="email"),
    path('logout/', customLogoutView.as_view(), name = "logout")
]