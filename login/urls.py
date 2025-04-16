from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register, loginCustomer, custom_logout

app_name = 'login'

urlpatterns = [
    path("register/", register, name="register"),
    path('', loginCustomer, name='login'),
     path('logout/', custom_logout, name='logout'),
]
