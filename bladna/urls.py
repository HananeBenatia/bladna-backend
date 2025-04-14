from django.urls import path 
from .views import user_login , user_signin

urlpatterns = [
    path('signin/', user_signin.as_view() , name = 'SignIn'),
    path('login/', user_login.as_view() , name = 'LogIn'),
]

