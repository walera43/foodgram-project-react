from django.contrib.auth.models import AbstractUser
from django.db import models
from .validations import HEX_valid
from ..users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    measurement_unit = models.CharField(max_length=200)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=200, validators=[HEX_valid])
    slug = models.SlugField(unique=True)


class Recipe(models.Model):
    ingredients = models.ManyToManyField(Ingredient)
    tags = models.ManyToManyField('Tag', related_name='recipes')
    name = models.CharField(max_length=200)
    text = models.TextField(verbose_name='Описание рецепта')
    cooking_time = models.IntegerField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
