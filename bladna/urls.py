from django.urls import path 
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import user_login , user_signin , secret_answer_set , secret_answer_verify ,SaveprogressView ,get_today_progress
urlpatterns = [
    path('signin/', user_signin.as_view() , name = 'SignIn'),
    path('login/', user_login.as_view() , name = 'LogIn'),
    path('set_parent_secret/', secret_answer_set.as_view() , name = 'Set_Parent_secret_answer'),
    path('verify_parent_secret/', secret_answer_verify.as_view() , name = 'verify_Parent_secret_answer'),
    path('progress/save/', SaveprogressView.as_view() , name = 'save_progress'),
    path('progress/today/', get_today_progress , name = 'get_today_progress'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]

