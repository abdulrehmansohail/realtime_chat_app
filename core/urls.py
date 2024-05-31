from django.urls import path
from core.views import (
    UserDetailView,
    RegistrationView,
    EmailExistAPIView,
    ForgetPasswordView,
    ChangePasswordView,
    ResetPasswordAPIView,
    AccountActivationAPIView,
)
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import ObtainJSONWebToken

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('account/activation/<secret_key>', AccountActivationAPIView.as_view(),
         name='account-activation'),
    path('login/', ObtainJSONWebToken.as_view(), name='token_obtain_pair'),
    path('me/', UserDetailView.as_view(), name='user'),
    path('forget/password/', ForgetPasswordView.as_view(), name='forget_password'),


    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    
   
    path('reset/password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('email-exist/', EmailExistAPIView.as_view(), name='email-exist'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

]
