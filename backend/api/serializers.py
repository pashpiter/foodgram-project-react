from django.db.models import F
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST


from recipes.models import (Ingredient, IngredientInRecipe, IsFavorited,
                            IsInShippingCart, RecipeList, Tag)
from user.serializers import UserRegistrationSerializer

from .utils import create_update_ingredients_in_recipe


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер для тегов"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientsInRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для добавления ингредиентов в рецепт"""
    id = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('__all__')
        read_only_fields = (
            'recipe', 'ingredient_in_recipe', 'measurement_unit'
        )


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериалайзер для ингредиентов"""

    class Meta:
        model = Ingredient
        fields = ('__all__')
        read_only_fields = ('name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для рецептов"""
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    author = UserRegistrationSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField()

    class Meta:
        model = RecipeList
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')
        read_only_fields = ('author', 'is_favorited', 'is_in_shopping_cart')

    def get_ingredients(self, obj):
        return obj.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('in_ingredient__amount')
        )

    def validate(self, data):
        ingredients = self.initial_data['ingredients']
        if len(ingredients) == 0:
            raise serializers.ValidationError(
                {'ingredients': ('Рецепт не может быть без ингредиентов!')},
                code=HTTP_400_BAD_REQUEST
            )
        ingredient_list = []
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient, pk=ingredient.get('id')
            )
            if current_ingredient in ingredients:
                raise serializers.ValidationError(
                    {'ingredients': ('Ингредиенты не могут повторяться!')},
                    code=HTTP_400_BAD_REQUEST
                )
            if int(ingredient.get('amount')) > 10000:
                raise serializers.ValidationError(
                    {'ingredients': ('Количество не может быть больше 10000')},
                    code=HTTP_400_BAD_REQUEST
                )
            ingredient_list.append(current_ingredient)
        data.update({
            'ingredients': ingredients,
            'tags': self.initial_data['tags']
        })
        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = RecipeList.objects.create(**validated_data)
        recipe.tags.add(*tags)
        create_update_ingredients_in_recipe(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        if tags:
            instance.tags.clear()
            instance.tags.set(tags)

        if ingredients:
            instance.ingredients.clear()
            create_update_ingredients_in_recipe(instance, ingredients)

        instance.save()
        return instance

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        fav_recipe = IsFavorited.objects.filter(fav_recipe=obj)
        if not fav_recipe:
            return False
        follower = self.context['request'].user
        return fav_recipe.filter(follower=follower).exists()

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        food_list = IsInShippingCart.objects.filter(food_list=obj)
        if not food_list:
            return False
        user_cart = self.context['request'].user
        return food_list.filter(user_cart=user_cart).exists()


class IsFavoriteSerializer(serializers.ModelSerializer):
    """Сериалайзер для избранного"""

    class Meta:
        model = IsFavorited
        fields = ('id', 'fav_recipe', 'follower')
        read_only_fields = ('fav_recipe', 'follower')

    def to_representation(self, instance):
        recipe = RecipeList.objects.get(id=instance.fav_recipe_id)
        data = super(IsFavoriteSerializer, self).to_representation(
            instance.fav_recipe.id)
        data['id'] = instance.pk
        data['name'] = recipe.name
        data['image'] = recipe.image.url
        data['cooking_time'] = recipe.cooking_time
        return data


class IsInShippingCartSerializer(serializers.ModelSerializer):
    """Сериалайзер для корзины"""

    class Meta:
        model = IsInShippingCart
        fields = ('food_list', 'user_cart')
        read_only_fields = ('food_list', 'user_cart')

    def to_representation(self, instance):
        recipe = RecipeList.objects.get(id=instance.food_list_id)
        data = super(IsInShippingCartSerializer, self).to_representation(
            instance.food_list.id)
        data['id'] = instance.pk
        data['name'] = recipe.name
        data['image'] = recipe.image.url
        data['cooking_time'] = recipe.cooking_time
        return data
