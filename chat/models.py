from django.db import models
from core.models import User


# Create your models here.


# ####### One To One Private Chats ########


class Room(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_rooms')
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partner_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RoomMessage(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='room_messages', null=True, blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owner_room_messages', null=True, blank=True)
    message = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# ####### Group Chats ########
class GroupRoom(models.Model):
    group_members = models.ManyToManyField(User, related_name='members')
    group_admin = models.ForeignKey(User, related_name='group_room_admin', on_delete=models.CASCADE)
    group_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name


class GroupRoomMessage(models.Model):
    room = models.ForeignKey(
        GroupRoom, on_delete=models.CASCADE, related_name='ws_room_messages')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='profile_ws_room_messages')
    message = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
