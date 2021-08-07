from django.contrib.auth import models
from rest_framework import serializers
from .models import Ingredient, Recipe, Tag

class IngredientsSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField()
    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id']


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    ingridients = IngredientsSerializer(many=True)
    tags = TagsSerializer(many=True)
    class Meta:
        model = Recipe
        fields = ('ingridients', 'tags', 'name', 'text', 'cooking_time', 'author')


class TagsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')




