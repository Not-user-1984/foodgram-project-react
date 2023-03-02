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
        'name',
        'amount_favorites',
        'amount_tags',
        'amount_ingredients'
        )

    search_fields = ('name',)
    inlines = [IngredientAmountInline]

    @staticmethod
    def amount_favorites(obj):
        return obj.favorites.count()

    @staticmethod
    def amount_tags(obj):
        return "\n".join([i[0] for i in obj.tags.values_list('name')])

    @staticmethod
    def amount_ingredients(obj):
        return "\n".join([i[0] for i in obj.ingredients.values_list('name')])


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
