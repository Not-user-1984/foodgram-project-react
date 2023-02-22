from foodgram.models import Ingredient, IngredientQuantity, Recipe, Tag
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .serializers import (IngredientSerializer,
                          RecipeSerializer, TagSerializer)


class IngredientsViewsSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ReadOnlyModelViewSet):
    queryset = Recipe
    serializer_class = RecipeSerializer
