from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True},
                        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
