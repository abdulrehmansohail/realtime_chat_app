from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from chat.models import GroupRoom
from .serializers import GroupRoomSerializer


class GroupRoomViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = GroupRoom.objects.all()
    serializer_class = GroupRoomSerializer

    def get_queryset(self):
        user = self.request.user
        return GroupRoom.objects.filter(group_members=user)

    def create(self, request, *args, **kwargs):
        serializer = GroupRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.group_admin == request.user:
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'message': "you are not allowed to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.group_admin == request.user:
            instance.delete()
            return Response({"message": "Group deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': "you are not allowed to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)


class AddAndRemoveGroupMemberAPIView(UpdateAPIView):
    """
    This View is used to add and remove the members of the group
    permission_classes:
        IsAuthenticated
    Parameters:
        id: int
    Returns:
        profile: object

    """
    serializer_class = GroupRoomSerializer
    model = GroupRoom
    lookup_field = 'pk'

    def get_queryset(self):
        return GroupRoom.objects.filter(group_members=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.group_admin == request.user:
            is_remove = request.data.get('is_remove', None)
            if (instance.group_admin == request.user) and is_remove:
                return Response({'message': "You are not be able to remove admin from group..."},
                                status=status.HTTP_401_UNAUTHORIZED)
            if is_remove:
                instance.group_members.remove(request.data.get('member'))
            else:
                if instance.group_members.filter(id=request.data.get('member')).exists():
                    return Response({'message': "This user is already member of this group..."},
                                    status=status.HTTP_401_UNAUTHORIZED)
                instance.group_members.add(request.data.get('member'))
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'message': "you are not allowed to perform this action"},
                status=status.HTTP_401_UNAUTHORIZED
            )
