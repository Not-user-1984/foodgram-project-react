from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, UserManager)
from django.db import models
from foodgram.models import Recipe


class User(AbstractBaseUser, PermissionsMixin):
    """
    Добавлен вход по email
    """

    email = models.EmailField(
        verbose_name='Электроная почта',
        unique=True,
        max_length=settings.LIMIT_EMAIL
        )
    username = models.CharField(
        verbose_name='Никнейм',
        max_length=settings.LIMIT_USERNAME,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.LIMIT_USERNAME,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.LIMIT_USERNAME,
        )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class CustomUserManager(BaseUserManager):
    """
    Кастомная мoдель Менеджера создания пользователя
    """
    def create_superuser(
            self, email, username, first_name, last_name,
            password, **other_fields
    ):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if not other_fields.get("is_staff"):
            raise ValueError("в доступе отказано")

        if not other_fields.get("is_superuser"):
            raise ValueError("в доступе отказано")

        return self.create_user(
            email, username, first_name, last_name,
            password=password, **other_fields
        )

    def create_user(self, first_name, last_name,
                    email, password, **other_fields):
        if not email:
            raise ValueError("укажите email")

        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name,
            last_name=last_name, **other_fields
        )
        user.set_password(password)
        user.save()
        return user


class Follow(models.Model):
    """
    Подписки пользователя
    """
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow',
            )
        ]


class Cart(models.Model):
    """
    Корзина пользователя
    """
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_shopping_cart')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='favorites',
        to=User,
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='favorites',
        to=Recipe,
        verbose_name='рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'избранные рецепты'

    def str(self):
        return f'{self.user} добавил {self.recipe} в список избранных'
