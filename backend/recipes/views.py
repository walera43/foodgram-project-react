from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from backend.recipes.models import (FavoriteRecipe, Ingredient,
                                    IngredientRecipe, Recipe,
                                    ShoppingCartRecipe, Tag)
from backend.recipes.permissions import IsAuthorOrIsAdminOrReadOnly

from .filters import IngredientFilter, RecipeFilter
from .serializers import (IngredientsSerializer, RecipeCreateSerializer,
                          RecipeSerializer, RecipeSerializerShort,
                          TagsListSerializer)


class ReciepsViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrIsAdminOrReadOnly
    ]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeCreateSerializer

    @action(methods=['GET', 'DELETE'], detail=True, url_path='favorite')
    def favorite(self, request, pk):
        current_user = request.user
        current_recipe = get_object_or_404(Recipe, id=pk)
        if self.request.method == 'GET':
            obj, created = FavoriteRecipe.objects.get_or_create(
                user=current_user,
                recipe=current_recipe
            )
            if not created:
                return Response(
                    'Рецепт уже есть в вашем списке избранных',
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = RecipeSerializerShort(current_recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        to_delete = get_object_or_404(
            FavoriteRecipe,
            user=current_user,
            recipe=current_recipe
        )
        to_delete.delete()
        return Response(
            'Удалено!',
            status=status.HTTP_204_NO_CONTENT
        )

    @action(methods=['GET', 'DELETE'], detail=True, url_path='shopping_cart')
    def shopping_cart(self, request, pk):
        current_user = request.user
        current_recipe = get_object_or_404(Recipe, id=pk)
        if self.request.method == 'GET':
            obj, created = ShoppingCartRecipe.objects.get_or_create(
                user=current_user,
                recipe=current_recipe
            )
            if not created:
                return Response(
                    'Рецепт уже есть в вашем списке избранных',
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = RecipeSerializerShort(current_recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        to_delete = get_object_or_404(
            ShoppingCartRecipe,
            user=current_user,
            recipe=current_recipe
        )
        to_delete.delete()
        return Response(
            'Удалено!',
            status=status.HTTP_204_NO_CONTENT
        )

    @action(methods=['GET'], detail=False, url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        cart = request.user.shopping_cart.all()
        to_buy_list = {}

        for item in cart:
            ingredients = IngredientRecipe.objects.filter(recipe=item.recipe)
            for ingredient in ingredients:
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                amount = ingredient.amount

                if name not in to_buy_list:
                    to_buy_list[name] = {
                        'amount': amount,
                        'measurement_unit': measurement_unit,
                    }
                else:
                    to_buy_list[name]['amount'] = (to_buy_list[name]['amount']
                                                   + amount)

        download_list = []
        postition = 1
        for item in to_buy_list:
            download_list.append(f'{postition}.{item} - '
                                 f'{to_buy_list[item]["amount"]} '
                                 f'{to_buy_list[item]["measurement_unit"]}.\n')
            postition += 1
        download_list.append(f'Всего к покупке {postition - 1} продукта(-ов)!')

        response = HttpResponse(download_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="buy_list.txt"'
        return response


class TagsListViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsListSerializer
    permission_classes = [AllowAny, ]
    pagination_class = None


class IngredientListViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = IngredientFilter
    pagination_class = None
