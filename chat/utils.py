from django.db.models import Q
from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async
from django.template.defaultfilters import slugify

from .models import (
    Room,
    RoomMessage,
    GroupRoom,
    GroupRoomMessage,
)
from .serializers import (
    ListRoomSerializer,
    RoomMessageSerializer,
    GroupRoomMessageSerializer,
)



@database_sync_to_async
def get_chat_rooms_updated(user, request):
    """ 
        This function is used to get updated chat rooms of the user 
    """
    rooms = Room.objects.filter(
        Q(owner=user) | Q(partner=user)
    )
    rooms_serializer = ListRoomSerializer(
        rooms, many=True, context={'request': request, 'user': user})
    return rooms_serializer.data


@database_sync_to_async
def is_group_room_member(user, group):
    """
        This function is used to check whether the user is the
        member of the workspace room or not.
    """
    try:
        group = GroupRoom.objects.get(id=group)
        is_member = group.group_members.filter(id=user.id).exists()
        return is_member, group
    except:
        return False, None


@database_sync_to_async
def create_ws_room_msg_object(workspace, user, message):
    workspace_room = get_object_or_404(GroupRoom, id=workspace)
    _attachment = None

    message_obj = GroupRoomMessage.objects.create(
        room=workspace_room,
        user=user,
        message=message,
    )
    message_ser = GroupRoomMessageSerializer(message_obj)
    return message_ser.data


@database_sync_to_async
def is_room_member(user, room_id):
    """
        This function is used to check weather the user is the
        member of the room or not.
    """
    rooms = Room.objects.filter(
        Q(id=room_id) & (Q(owner=user) | Q(partner=user))
    )
    if rooms.exists():
        room = rooms.first()
        group_name = slugify(
            f'{room.owner.username}-'
            f'{room.partner.username}-{room.id}')
        return True, group_name
    return False, None


search_field_for_partner = [
    'partner__last_name',
    'partner__first_name',
    'partner__username',
]


@database_sync_to_async
def create_room_message_object(room, message, user):
    """
        This function is used to create the instance of RoomMessage class
        when the message in set in private chat
    """
    room = get_object_or_404(Room, id=room)
    message_obj = RoomMessage.objects.create(
        room=room,
        owner=user,
        message=message
    )
    message_ser = RoomMessageSerializer(message_obj)
    return message_ser.data
