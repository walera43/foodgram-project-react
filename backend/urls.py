from django.contrib import admin
from django.urls import path, include
from rest_framework import urlpatterns
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .users.views import UserViewSet
from .recipes.views import ReciepsViewSet, TagsListViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('recipes', ReciepsViewSet, basename='recipes')
router.register('tags', TagsListViewSet, basename='tags')


urlpatterns = [
    path('', include(router.urls)),
]
