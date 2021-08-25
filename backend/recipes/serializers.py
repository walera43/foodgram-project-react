from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from ..users.models import User
from .models import (FavoriteRecipe, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCartRecipe, Tag)


class UserShow(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientsAddRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class IngredientShowInRecipe(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(read_only=True, source="ingredient.name")
    measurement_unit = serializers.CharField(
        read_only=True,
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id',)


class TagsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserShow()
    tags = TagsListSerializer(many=True, read_only=True)
    ingredients = IngredientShowInRecipe(many=True,
                                         source='ingredientrecipe_set')
    is_favorited = serializers.SerializerMethodField(
        'get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        'get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        current_user = self.context['request'].user
        current_recipe = get_object_or_404(Recipe, id=obj.id)
        return (
            current_user.is_authenticated and FavoriteRecipe.objects.filter(
                user=current_user,
                recipe=current_recipe.id).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        current_user = self.context['request'].user
        current_recipe = get_object_or_404(Recipe, id=obj.id)
        return (
            current_user.is_authenticated
            and ShoppingCartRecipe.objects.filter(
                user=current_user,
                recipe=current_recipe.id).exists()
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=True
    )
    ingredients = IngredientsAddRecipeSerializer(many=True)
    image = Base64ImageField(
        max_length=300,
        use_url=True
    )

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'image', 'name', 'text',
                  'cooking_time', 'author')

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        to_check = []
        for ingredient in ingredients:
            if ingredient['id'] in to_check:
                raise serializers.ValidationError(
                    'Ингредиенты не должны повторяться!'
                )
            to_check.append(ingredient['id'])
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError(
                    {'amount': 'Значение не может быть '
                               'меньше 0'}
                )
        data['ingredients'] = ingredients
        tags = self.initial_data.get('tags')
        if len(tags) == 0:
            raise serializers.ValidationError(
                'Поставьте хотя бы один тег!'
            )
        data['tags'] = tags
        return data

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags_data)
        recipe.save()
        for ingredient in ingredients_data:
            current_id = ingredient['id']
            current_amount = ingredient['amount']
            IngredientRecipe.objects.create(
                ingredient_id=current_id,
                recipe=recipe,
                amount=current_amount
            )
        return recipe

    def to_representation(self, instance):
        return RecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        ingredient_data = validated_data.pop('ingredients')
        IngredientRecipe.objects.filter(recipe=instance).delete()
        for new_ingredient in ingredient_data:
            IngredientRecipe.objects.create(
                ingredient=new_ingredient['id'],
                recipe=instance,
                amount=new_ingredient['amount']
            )
        instance.tags.set(tags_data)
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        if validated_data.get('image') is not None:
            instance.image = validated_data.pop('image')
        instance.cooking_time = validated_data.pop('cooking_time')
        instance.save()
        return instance
