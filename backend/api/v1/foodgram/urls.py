from api.v1.foodgram.views import (IngredientsViewsSet, RecipeViewSet,
                                   TagsViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewsSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
]
