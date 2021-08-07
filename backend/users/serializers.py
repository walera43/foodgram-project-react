from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import User


class UserCreateSerializer(UserCreateSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password',)