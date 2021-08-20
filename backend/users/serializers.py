from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from ..recipes.serializers import RecipeSerializerShort
from .models import Subscribe, User


class UserCreateSerializer(UserCreateSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'password',)


class UserDetailSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=request.user, author=obj).exists()


class SubscribeSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        author = get_object_or_404(User, id=obj.id)
        return Subscribe.objects.filter(user__follower__author=author)

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializerShort(
            recipes,
            many=True,
            context=context).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
