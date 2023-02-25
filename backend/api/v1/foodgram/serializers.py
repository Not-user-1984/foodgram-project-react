from api.v1.users.serializers import CustomUserSerializer
from drf_extra_fields.fields import Base64ImageField
from foodgram.models import Ingredient, IngredientQuantity, Recipe, Tag
from rest_framework import serializers
from users.models import Cart, Favorite


class IngredientSerializer(serializers.ModelSerializer):
    """
    Игредиенты рецепта.
    """
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            )
        read_only_fields = (
            'id',
            'name',
            'measurement_unit',
            )


class TagSerializer(serializers.ModelSerializer):
    """
    теги рецепта
    """
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
            )
        read_only_fields = (
            'id',
            'name',
            'color',
            'slug'
            )


class IngredientListRecipeSerializer(serializers.ModelSerializer):
    """
    сделан переход на вторую таблицу Ingredient.
    вспомогательный сериализатор для RecipeListSerializer.
    """
    id = serializers.ReadOnlyField(source='ingredient.it')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    quantity = serializers.IntegerField()

    class Meta:
        model = IngredientQuantity
        fields = (
            'id',
            'name',
            'measurement_unit',
            'quantity'
            )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """
    вспомогательный сериализатор для RecipeSerializer.
    """
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    quantity = serializers.IntegerField()

    class Meta:
        model = IngredientQuantity
        fields = ('id', 'quantity')


class RecipeListSerializer(serializers.ModelSerializer):
    """
    при запросе на список рецептов
    """
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'is_in_shopping_cart',
            'is_favorited',
            )

    def get_ingredients(self, obj):
        queryset = IngredientQuantity.objects.filter(recipe=obj)
        return IngredientListRecipeSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Cart.objects.filter(
            user=request.user, recipe=obj).exists()


class RecipeSerializer(serializers.ModelSerializer):
    """
    при запросе на один рецепт
    """
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
        )
    ingredients = IngredientRecipeSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            )

    def validate(self, data):
        ingredients = data['ingredients']
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError({
                    'ingredients': 'ингредиенты должны быть уникальными '
                })

        tags = data['tags']
        if not tags:
            raise serializers.ValidationError({
                'tags': 'нужно выбрать хотя бы один тэг'
            })

        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError({
                    'tags': 'тэги должны быть уникальными'
                })
            tags_list.append(tag)
        return data

    @staticmethod
    def create_tags(tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    @staticmethod
    def create_ingredients(ingredients, recipe):
        for ingredient in ingredients:
            IngredientQuantity.objects.create(
                recipe=recipe, ingredient=ingredient['id'],
                quantity=ingredient['quantity']
            )

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=author,  **validated_data
        )
        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientQuantity.objects.filter(recipe=instance).data
        self.create_tags(validated_data.pop('tags'), instance)
        self.create_ingredients(validated_data.pop('ingredients'), instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeListSerializer(instance, context=context).data
