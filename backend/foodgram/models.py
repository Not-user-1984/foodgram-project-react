from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from django.db import models

User = get_user_model


class Ingredient(models.Model):
    """
    Таблица Игредиентов имеет связь
    с таблицей 'Рецепт' многие к многим.
    """
    name = models.CharField(
        verbose_name="Название игредиента",
        max_length=settings.LIMIT_USERNAME,
    )
    measurement_unit = models.CharField(
        verbose_name="Единица измериния",
        max_length=settings.LIMIT_UNIT,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]
        ordering = ('name',)
        verbose_name = 'Игредиент'
        verbose_name_plural = 'Игредиенты'

    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    """
    Вспомагательная Таблица 'Количество ингредиентов' имеет связь
    с таблицей 'Рецепт' один к многим,
    c таблицей 'Игредиентов'один к многим,
    """
    recipe = models.ForeignKey(
        to='Recipe',
        on_delete=models.CASCADE,
        related_name='quantity',
        verbose_name='Рецепт'

    )
    ingredient = models.ForeignKey(
        to='Ingredient',
        on_delete=models.CASCADE,
        related_name='quantity',
        verbose_name='Ингредиент'
    )
    quantity = models.BigIntegerField(
        'Количество Игрендиета',
        validators=(
            MinValueValidator(
                    settings.MIN_LIMIT,
                    message='Количество не меньше 1'
                    ),
                )
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredient_amount',
            ),
        )


class Tag (models.Model):
    """
    Таблица Тегов имеет связь
    с таблицей 'Рецепт' многие к многим.
    """
    name = models.CharField(
        verbose_name="тег",
        max_length=settings.LIMIT_USERNAME,
    )
    color = models.CharField(
        verbose_name="цвет",
        max_length=10,
    )
    slug = models.SlugField(
        verbose_name='Url',
        unique=True,
        max_length=settings.LIMIT_SLUG,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe (models.Model):
    """
    Таблица Рeценты имеет связь
    с таблицей 'Тег' многие к многим,
    с таблицей 'Игредиенты' многие к многим, через 'Количество ингредиентов',
    c таблицей 'Пользователя' один ко многим,
    """
    author = models.ForeignKey(
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='recipes',
        to=settings.AUTH_USER_MODEL,

    )
    ingredients = models.ManyToManyField(
        verbose_name='Игредиенты',
        related_name='recipes',
        to=Ingredient,
        through=IngredientQuantity,
        blank=True,
    )
    tags = models.ManyToManyField(
        verbose_name='теги',
        related_name='recipes',
        to='Tag',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/'
    )
    name = models.CharField(
        verbose_name="названия",
        max_length=settings.LIMIT_USERNAME,
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.BigIntegerField(
        verbose_name='Время приготовления(мин.)',
        validators=(
            MinValueValidator(
                    settings.MIN_LIMIT,
                    message='Не меньше 1 минуты'
            ),
        )
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепт'

    def __str__(self):
        return self.name
