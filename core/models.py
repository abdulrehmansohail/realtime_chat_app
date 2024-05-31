from django.db import models
from coresite.mixin import AbstractTimeStampModel
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Please provide email")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("super user must have staff user")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Our custom user model that extends Django's AbstractBaseUser."""
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'username']

    def __str__(self):
        return self.email


class ForgetPassword(AbstractTimeStampModel):
    """
    Here you can reset your password in case you lost your password
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='forget_password', unique=True, primary_key=True)
    reset_email_token = models.CharField(max_length=255)
    activated = models.BooleanField(default=True)
    is_expired = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'ForgetPassword'


class UserActivation(AbstractTimeStampModel):
    """
    Here you can activate your account
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_activation', unique=True)
    otp = models.CharField(max_length=100, blank=True, null=True)
    activated = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'UserActivation'
