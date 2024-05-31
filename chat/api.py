from django.db.models import Q
from rest_framework import status
from rest_framework import filters
from rest_framework.views import Response
from .utils import search_field_for_partner
from utils.paginations import OurLimitOffsetPagination
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from .models import Room, RoomMessage, GroupRoomMessage
from .serializers import (
    ListRoomSerializer,
    CreateRoomSerializer,
    RoomMessageSerializer,
    GroupRoomMessageSerializer,

)

# Create your views here.


class GroupActivityPreviousChatView(ListAPIView):
    """
    This View is used to give the previous messages of group
    activity. If the workspace_is in query params is given then
    it will return the messages of that group room else it will
    return all the messages of all group rooms.
    permission_classes:
        IsAuthenticated
    Parameters:
        group_id: int
    Returns:
        messages: list

    """
    serializer_class = GroupRoomMessageSerializer
    pagination_class = OurLimitOffsetPagination

    def get_queryset(self):
        group_id = self.request.GET.get('group_id')
        if group_id:
            messages = GroupRoomMessage.objects.filter(
                room__id=group_id,
            ).order_by('-created_at')
            return messages
        messages = GroupRoomMessage.objects.all().order_by('-created_at')
        return messages


class CreateRoomView(CreateAPIView):

    """
    This View is used to create a room for personal chat between
    buyer and seller.
    permission_classes:
        IsAuthenticated
    Parameters:
        partner: int
        owner: int

    Returns:
        room: object

    """
    serializer_class = CreateRoomSerializer
    queryset = Room.objects.all()

    def get_serializer_context(self):
        context = {"request": self.request}
        return context


class ListRoomsView(ListAPIView):
    """
    This View is used return all rooms of the request's user.
        - If request's user is buyer, it will return all those rooms
          in which he is added as owner
        - If request's user is seller, it will return all those rooms
          in which he is added as partner
    permission_classes: 
        IsAuthenticated
    Parameters: 
        None
    search_fields:
        partner__user__first_name
        partner__user__last_name
        partner__user__username
    Returns:
        rooms: list

    """

    serializer_class = ListRoomSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = search_field_for_partner

    def get_queryset(self):
        rooms = Room.objects.filter(owner=self.request.user)
        return rooms

    def get_serializer_context(self):
        context = {
            "request": self.request,
            "user": self.request.user
        }
        return context


class RoomPreviousChatView(ListAPIView):

    """
    This View is used to give the previous messages of room
    permission_classes:
        IsAuthenticated
    Parameters:
        id: int
    Returns:
        messages: list

    """

    serializer_class = RoomMessageSerializer
    pagination_class = OurLimitOffsetPagination

    def list(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        try:
            messages = RoomMessage.objects.filter(
                room_id=id,
            ).order_by('-created_at')
            chat_list_serializer = self.serializer_class(messages, many=True)
            return Response(chat_list_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': "error",
                'status': status.HTTP_404_NOT_FOUND
            })
