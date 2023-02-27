from django.contrib import admin

from .models import Ingredient, IngredientQuantity, Recipe, Tag


class IngredientAmountInline(admin.TabularInline):
    model = IngredientQuantity
    min_num = 1


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name'
        )
    search_fields = ('name',)
    inlines = [IngredientAmountInline]


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
        'amount'
    )


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
        )
