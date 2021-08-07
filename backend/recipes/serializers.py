from rest_framework import serializers
from .models import Ingredient, Recipe, Tag, IngredientRecipe
from ..users.models import User


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')

#ДОРАБОТАТЬ!
class IngredientsRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id',)


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    #РАЗОБРАТЬСЯ!
    ingridients = IngredientsRecipeSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('ingridients', 'tags', 'name', 'text',
                  'cooking_time', 'author')

    def to_representation(self, instance):
       ret = super().to_representation(instance)
       ret['tags'] = TagsSerializer(instance.tags).data
       return ret

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super(RecipeCreateSerializer, self).create(validated_data)


class TagsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
