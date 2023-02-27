from django.contrib import admin

from .models import Cart, CustomUser, Favorite, Follow


@admin.register(CustomUser)
class AdminCustomUser(admin.ModelAdmin):
    """
    Для модели пользователей включена фильтрация по имени и email
    """
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        )
    search_fields = (
        'username',
        'email',
        )
    list_fields = (
        'username',
        'email',
        )


@admin.register(Follow)
class FollowRecipe(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'user',
        )
    search_fields = (
        'author',
        'user',
        )
    list_fields = (
        'author',
        'user',
        )


@admin.register(Cart)
class CartRecipe(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
        )
    search_fields = (
        'user',
        'recipe',
        )
    list_fields = (
        'user',
        'recipe',
        )


@admin.register(Favorite)
class AdnimFavorite(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe'
    )
