from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import (
    User,
    UserActivation,
    ForgetPassword,
)


@admin.register(ForgetPassword)
class ForgetPasswordAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'is_staff', 'is_active')
    list_display_links = ('id', 'email', 'username')
    search_fields = ('email', 'username')
    list_filter = ('is_staff', 'is_active')
    list_per_page = 25


@admin.register(UserActivation)
class UserActivationAdmin(admin.ModelAdmin):
    pass
