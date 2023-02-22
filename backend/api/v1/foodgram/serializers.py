from foodgram.models import Ingredient, IngredientQuantity, Recipe, Tag
from rest_framework import serializers
from api.v1.users.serializers import CustomUserSerializer
from users.models import Cart, Favorite
from drf_extra_fields.fields import Base64ImageField


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fienlds = (
            'id',
            'name',
            'measurement_unit',
            )
        read_only_fields = '__all__',


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fienlds = (
            'id',
            'name',
            'color',
            'slug'
            )
        read_only_fields = '__all__',


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
        fienlds = (
            'id',
            'name',
            'measurement_unit',
            'quantity'
            )
        read_only_fields = '__all__'


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
            'name',
            'image',
            'description',
            'tags',
            'cooking_time',
            'pub_date'
            )

    def get_ingredients(self, obj):
        queryset = IngredientListRecipeSerializer.objects.filter(recipe=obj)
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
        # посмотреть валидацию по тз
        tags = self.initial_data['tags']
        if not tags:
            raise serializers.ValidationError(
                'Нужно добавить хотя бы 1 тэг'
            )
        ingredients = self.initial_data['ingredients']
        if not ingredients:
            raise serializers.ValidationError(
                'Нужно добавить хотя бы 1 ингредиент'
            )

        for value in (tags, ingredients):
            if not isinstance(value, list):
                raise serializers.ValidationError(
                    f'{value} должен быть в формате list'
                )

        for ingredient in ingredients:
            if not ingredient['amount'].isdecimal():
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть числом'
                )
            if not (1 <= int(ingredient['amount']) <= 10000):
                raise serializers.ValidationError(
                    'Количество ингредиента может быть от 1 до 10000'
                )
        if not (1 <= int(self.initial_data['cooking_time']) <= 1000):
            raise serializers.ValidationError(
                'Время приготовление может быть от 1 до 1000'
            )
        data['tags'] = tags
        data['ingredients'] = ingredients
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
