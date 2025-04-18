from django.urls import path 
from .views import user_login , user_signin , secret_answer_set , secret_answer_verify 

urlpatterns = [
    path('signin/', user_signin.as_view() , name = 'SignIn'),
    path('login/', user_login.as_view() , name = 'LogIn'),
    path('set_parent_secret/', secret_answer_set.as_view() , name = 'Set_Parent_secret_answer'),
    path('verify_parent_secret/', secret_answer_verify.as_view() , name = 'verify_Parent_secret_answer'),
]

