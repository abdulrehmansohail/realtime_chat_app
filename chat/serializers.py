from rest_framework import serializers
from .models import (
    Room,
    GroupRoom,
    RoomMessage,
    GroupRoomMessage,
)


class GroupRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupRoom
        fields = '__all__'


class GroupRoomMessageSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = GroupRoomMessage
        fields = '__all__'


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    def validate(self, attrs):
        owner = attrs.get('owner')
        request = self.context.get('request')
        if owner != request.user:
            raise serializers.ValidationError(
                "Invalid owner, give requested user's id in owner")

        return super().validate(attrs)

    def create(self, validated_data):
        owner = validated_data.get('owner')
        room = Room.objects.filter(owner=owner).first()
        if room:
            return room
        return super().create(validated_data)


class ListRoomSerializer(serializers.ModelSerializer):

    """
        This serializer is used to list the updated chat rooms of the user
    """

    response = serializers.SerializerMethodField()

    def get_response(self, obj):

        user = self.context.get('user')

        try:
            partner = {}

            ### dynamic fields for the UPDATE ROOM API of the partners ###

            partner['partner_id'] = obj.partner.id
            partner['room_id'] = obj.id
            partner['partner_username'] = obj.partner.username
            partner['partner_first_name'] = obj.partner.first_name
            partner['partner_last_name'] = obj.partner.last_name
            room_message = RoomMessage.objects.filter(
                room=obj,
            ).last()
            if room_message:
                partner['last_message'] = room_message.message
                partner['last_message_time'] = room_message.created_at

                if room_message.owner == user:
                    partner['is_my_msg'] = True
                else:
                    partner['is_my_msg'] = False
            else:
                partner['partner_last_message'] = None

            ### dynamic fields for the UPDATE ROOM API of the owner ###

            partner['room_created_at'] = obj.created_at.strftime(
                "%Y-%m-%d %H:%M:%S")
            partner['owner_id'] = obj.owner.id
            partner['room_id'] = obj.id
            partner['owner_username'] = obj.owner.username
            partner['owner_first_name'] = obj.owner.first_name
            partner['owner_last_name'] = obj.owner.last_name
            # partner['owner_image'] = obj.owner.image.url if obj.owner.image else None
            room_message = RoomMessage.objects.filter(
                room=obj,

            ).last()

            if room_message:
                partner['last_message'] = room_message.message
                partner['last_message_time'] = room_message.created_at.strftime(
                    "%Y-%m-%d %H:%M:%S")

                if room_message.owner == user:
                    partner['is_my_msg'] = True

                else:
                    partner['is_my_msg'] = False

            else:
                partner['owner_last_message'] = None

            return partner
        except Exception as e:
            raise Exception(e)

    class Meta:
        model = Room
        fields = ['response']


class RoomMessageSerializer(serializers.ModelSerializer):
    """
        This serializer is used to list the messages of the room
    """

    first_name = serializers.CharField(
        source='owner.first_name', read_only=True)
    last_name = serializers.CharField(source='owner.last_name', read_only=True)

    class Meta:
        model = RoomMessage
        fields = '__all__'


class RoomMessageSerializer(serializers.ModelSerializer):
    """
        This serializer is used to list the messages of the room

    """
    last_name = serializers.CharField(source='owner.last_name', read_only=True)
    first_name = serializers.CharField(
        source='owner.first_name', read_only=True)
    user_name = serializers.CharField(
        source='owner.username', read_only=True)

    class Meta:
        model = RoomMessage
        fields = [
            'id',
            'room',
            'owner',
            'message',
            'last_name',
            'user_name',
            'first_name',
            'created_at',
            'updated_at',
        ]
