from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.v1.foodgram.filters import IngredientSearchFilter, RecipeFilter
from api.v1.foodgram.serializers import (IngredientSerializer,
                                         RecipeListSerializer,
                                         RecipeSerializer, TagSerializer)
from api.v1.pagination import NoNumberPagition, PageCastomNumberPagition
from api.v1.permissions import IsAthorOrReadOnly
from api.v1.users.serializers import CartSerializer, FavoriteSerialiser
from foodgram.models import Ingredient, IngredientQuantity, Recipe, Tag
from users.models import Cart, Favorite


class IngredientsViewsSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    pagination_class = (AllowAny)
    serializer_class = IngredientSerializer
    filter_backends = [IngredientSearchFilter]
    search_fields = ('^name',)
    pagination_class = NoNumberPagition


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    pagination_class = (AllowAny)
    serializer_class = TagSerializer
    pagination_class = NoNumberPagition


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = PageCastomNumberPagition

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    def post_actions(self, request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_actions(self, request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.post_actions(
            request=request, pk=pk, serializers=FavoriteSerialiser)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_actions(
            request=request, pk=pk, model=Favorite)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.post_actions(
            request=request, pk=pk, serializers=CartSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_actions(
            request=request, pk=pk, model=Cart)

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        pagination_class=None,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientQuantity.objects.filter(
            recipe__carts__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(total=Sum('amount'))
        shopping_list = 'Список покупок:\n'
        for ingredient in ingredients:
            shopping_list += ''.join([
                f'{ingredient["ingredient__name"]} - {ingredient["total"]}/'
                f'{ingredient["ingredient__measurement_unit"]} \n'
            ])
        file_name = 'Список покупок'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename="{file_name}.txt"'
        )
        return response
