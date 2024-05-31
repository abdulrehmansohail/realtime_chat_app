import logging as loggers
from rest_framework import status
from core.models import UserActivation
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from core.serializers import ChangePasswordSerializer
from core.serializers import UserDetailSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from core.models import ForgetPassword
from core.utils.reset_email_token_util import reset_email_token
from utils.threads import send_mail
from core.serializers import CreateUserSerializer
from datetime import datetime, timedelta, timezone

User = get_user_model()


loggers.basicConfig(level=loggers.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = loggers.getLogger(__name__)


email = settings.EMAIL_HOST_USER
react_domain = settings.REACT_DOMAIN
domain = settings.DOMAIN


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """User detail api instant """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ResetPasswordAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Parameters:
            email
            password
            otp
        """
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        otp = request.data.get('otp', '')
        if email and password and otp:
            user = get_object_or_404(User, email=email)

            token = get_object_or_404(ForgetPassword, user=user)

            if (token.created_at+timedelta(minutes=15)).replace(tzinfo=timezone.utc) < datetime.now(timezone.utc) - timedelta(minutes=15):

                token.activated = False
                token.is_expired = True
                token.save()
                return Response({"message": "OTP expired", "status": "400"}, status=status.HTTP_400_BAD_REQUEST)

            if token.reset_email_token == otp and token.activated and not token.is_expired:
                user.set_password(password)
                user.save()
                token.delete()
                return Response({"message": "Password reset successfully", "status": "200"}, status=status.HTTP_200_OK)
            return Response({"message": "Invalid OTP Regenerate OTP", "status": "400"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Email, Password and OTP are required", "status": "400"}, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(APIView):
    """REgister and login api instant """

    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Registering New User
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Sending Email for email varification
        instance = serializer.instance
        secret_key = reset_email_token(50)
        user_activation, _ = UserActivation.objects.get_or_create(user=instance)
        user_activation.otp = secret_key
        user_activation.is_expired = False
        user_activation.activated = False
        user_activation.save()

        key = {
            'username': instance.username,
            'otp': None, 'button': domain + '/api/user/account/activation/' + secret_key
        }

        subject = "Verify Your Account"
        template_name = "auth/new_userRegister.html"
        recipient = [request.data['email']]

        send_mail(subject=subject, html_content=template_name,
                  recipient_list=recipient, key=key)

        return Response({
            "message": "User created successfully. Check your email for verification"
        }, status=status.HTTP_201_CREATED)


class ForgetPasswordView(APIView):
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request):
        try:
            email = request.data.get('email', '')
            otp = request.data.get('otp', True)

            if email is None or email == '':
                message = {'detail': 'Email is required to reset password'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            user = get_object_or_404(User, email=email)
            token_exists = ForgetPassword.objects.filter(user=user)
            token_exists.delete()
            current_reset_token = reset_email_token(50, otp)
            token = ForgetPassword.objects.create(
                user=user, reset_email_token=current_reset_token)
            key = {
                'username': user.username,
                'button': 'auth/reset-password/'+str(token.reset_email_token)
            }
            if otp:
                key.update({'otp': current_reset_token, 'button': None})
            send_mail(subject="Reset Your Password", html_content="auth/forgetPassword.html",
                      recipient_list=[email], key=key)
            return Response({'detail': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("%d", e)
            return Response({'detail': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


class EmailExistAPIView(APIView):
    permission_classes = [AllowAny,]

    """ 
        Here you can check if email already exists or not
    """

    def post(self, request):
        try:
            """
            Parameters:
                email
            """
            if User.objects.filter(email=request.data['email']).exists():
                return Response({"message": False, "status": "400"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': True, "status": "200"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "status": "500"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChangePasswordView(generics.UpdateAPIView):
    """Change password api instant """
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',

            }
            key = {
                'username': self.object.username,
                'button': settings.REACT_DOMAIN+'auth/login',
            }
            send_mail(subject="Password Changed", html_content="auth/passwordChanged.html",
                      recipient_list=[self.object.email], key=key)

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountActivationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, secret_key):
        try:
            """
            This api is used to activate user account
            Parameters:
                secret_key

                """

            user_activation = get_object_or_404(
                UserActivation, otp=secret_key)
            if user_activation:
                if user_activation.activated:
                    return Response({"message": "Account already activated", "status": "400"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if user_activation.otp == secret_key and not user_activation.is_expired:
                    user_activation.activated = True
                    user_activation.save()
                    user_activation.user.is_active = True
                    user_activation.user.save()

                    return Response({"message": "Account activated successfully", "status": "200"},
                                    status=status.HTTP_200_OK)
                return Response({"message": "Activation key is not valid", "status": "400"},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Invalid token", "status": "400"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message": "User Not Found", "status": "500"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
