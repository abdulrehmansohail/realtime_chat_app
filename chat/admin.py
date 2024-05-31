from django.contrib import admin
from .models import Room, RoomMessage, GroupRoom, GroupRoomMessage

# Register your models here.


@admin.register(GroupRoom)
class GroupRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_name', 'created_at']


@admin.register(GroupRoomMessage)
class GroupRoomMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'user', 'message', 'created_at']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'created_at']


@admin.register(RoomMessage)
class RoomMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'owner', 'message', 'created_at']
