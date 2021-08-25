from django.db import models

from ..users.models import User
from .validations import hex_valid, recipe_time_valid


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.name} {self.measurement_unit}'

    class Meta:
        ordering = ('name',)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=200, validators=[hex_valid])
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        ordering = ('name',)


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        related_name='recipes'
    )
    image = models.ImageField()
    name = models.CharField(max_length=200)
    text = models.TextField(verbose_name='Описание рецепта')
    cooking_time = models.PositiveIntegerField(
        validators=[recipe_time_valid]
    )
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    class Meta:
        ordering = ['-id']


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.ingredient}, {self.amount}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unigue_recipe_ingredient'
            )
        ]


class TagRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.tag}'


class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite'
    )
    constraints = [
        models.UniqueConstraint(
            name='unique_is_favorited',
            fields=['recipe', 'user']
        )
    ]


class ShoppingCartRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    constraints = [
        models.UniqueConstraint(
            name='unique_shopping_cart',
            fields=['recipe', 'user']
        )
    ]
