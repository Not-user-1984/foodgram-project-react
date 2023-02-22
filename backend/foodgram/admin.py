from django.contrib import admin

from .models import Ingredient, IngredientQuantity, Recipe, Tag


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name'
        )
    search_fields = ('name',)


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit'
        )
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(IngredientQuantity)
class AdminIngredientQuantity(admin.ModelAdmin):
    list_display = (
        'id',
        'ingredient',
        'recipe',
        'quantity'
    )


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
        )
