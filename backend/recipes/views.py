from backend.recipes.models import Recipe, Tag
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import RecipeCreateSerializer, TagsListSerializer


class ReciepsViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeCreateSerializer


class TagsListViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsListSerializer
    permission_classes = [IsAuthenticated]