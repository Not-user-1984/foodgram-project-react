from djoser.serializers import UserCreateSerializer, UserSerializer
from foodgram.models import Recipe
from rest_framework import serializers
from users.models import Cart, CustomUser, Favorite, Follow


class CustomUserSerializer(UserSerializer):
    """
    добавленно вирт поле is_subscribed для подписок.
    """
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=user, author=obj.id
            ).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    кастом создания пользователя.
    """
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            )
    extra_kwargs = {
        'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ListPecipesSerialiser(serializers.ModelSerializer):
    """
    вспомагательный(дочерний) сериализатор для Подписок.
    возращает упращенный список рецептов.
    """
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
            )


class FollowSerializer(CustomUserSerializer):
    """
    Возвращает авторов, на которых подписан текущий пользователь.
    вирт поле recipes_count кол-во рецептов.
    recipes с лимитом на кол-во рецептов от фронта.
    """
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'recipes',
            'is_subscribed',
            'recipes_count'
            )

    @staticmethod
    def get_recipes_count(obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return ListPecipesSerialiser(recipes, many=True).data


class CartSerializer(serializers.ModelSerializer):
    """
    Корзина пользователя.
    Использован дочерний ListPecipesSerialiser,
    для короткого отабражение списка.
    """
    class Meta:
        model = Cart
        fields = (
            'user',
            'recipe'
            )

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ListPecipesSerialiser(
            instance.recipe, context=context).data


class FavoriteSerialiser(serializers.ModelSerializer):
    """
    Избранное пользователя.
    Использован дочерний ListPecipesSerialiser,
    для короткого отабражение списка.
    """
    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe'
            )

    def validate(self, attrs):
        request = self.context.get('request')
        recipe = attrs['recipe']
        if not request or request.user.is_anonymous:
            return False
        if Favorite.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists():
            raise serializers.ValidationError(
                "Tакой рецепт уже есть :)"
            )
        return attrs

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ListPecipesSerialiser(
            instance.recipe, context=context).data
