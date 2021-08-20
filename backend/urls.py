from django.contrib import admin
from django.urls import include, path
from rest_framework import routers, urlpatterns
from rest_framework.routers import DefaultRouter

from .recipes.views import (IngredientListViewSet, ReciepsViewSet,
                            TagsListViewSet)
from .users.views import SubscriptionsViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('recipes', ReciepsViewSet, basename='recipes')
router.register('tags', TagsListViewSet, basename='tags')
router.register('ingredients', IngredientListViewSet, basename='ingredients')


urlpatterns = [
    path('users/subscriptions/', SubscriptionsViewSet.as_view()),
    path('', include(router.urls)),
]
