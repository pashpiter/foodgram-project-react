from django.db.models import F
from rest_framework import serializers

from recipes.models import (Ingridient, IngridientInRecipe, IsFavorited,
                            IsInShippingCart, RecipeList, Tag)
from user.serializers import UserRegistrationSerializer
from .utils import updateingridientsinrecipe


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngridientsInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngridientInRecipe
        fields = ('__all__')
        read_only_fields = (
            'recipe', 'ingridient_in_recipe', 'measurement_unit'
        )


class IngridientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingridient
        fields = ('__all__')
        read_only_fields = ('name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shipping_cart = serializers.SerializerMethodField()
    ingridients = serializers.SerializerMethodField()
    author = UserRegistrationSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = RecipeList
        fields = (
            'id', 'tags', 'author', 'ingridients', 'is_favorited',
            'is_in_shipping_cart', 'name', 'image', 'text', 'cooking_time')
        read_only_fields = ('author', 'is_favorited', 'is_in_shipping_cart')

    def get_ingridients(self, obj):
        return obj.ingridients.values(
            'id', 'name', 'measurement_unit', amount=F('in_ingridient__amount')
        )

    def validate(self, data):
        data.update({
            'ingridients': self.initial_data['ingridients'],
            'tags': self.initial_data['tags']
        })
        return data

    def create(self, validated_data):
        ingridients = validated_data.pop('ingridients')
        tags = validated_data.pop('tags')
        recipe = RecipeList.objects.create(**validated_data)
        recipe.tags.add(*tags)
        for ingridient in ingridients:
            current_ingridient = Ingridient.objects.get(id=ingridient['id'])
            IngridientInRecipe.objects.create(
                ingridient_in_recipe=current_ingridient, recipe=recipe,
                amount=ingridient['amount']
            )
            recipe.ingridients.add(
                current_ingridient,
                through_defaults={'amount': ingridient['amount']}
            )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingridients = validated_data.pop('ingridients')

        if tags:
            instance.tags.clear()
            instance.tags.set(tags)

        if ingridients:
            instance.ingridients.clear()
            updateingridientsinrecipe(instance, ingridients)

        instance.save()
        return instance

    def get_is_favorited(self, obj):
        fav_recipe = IsFavorited.objects.filter(fav_recipe=obj)
        if not fav_recipe:
            return False
        follower = self.context['request'].user
        return fav_recipe.filter(follower=follower).exists()

    def get_is_in_shipping_cart(self, obj):
        food_list = IsInShippingCart.objects.filter(food_list=obj)
        if not food_list:
            return False
        user_cart = self.context['request'].user
        return food_list.filter(user_cart=user_cart).exists()


class IsFavoriteSerializer(serializers.ModelSerializer):

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
        data['image'] = recipe.image
        data['cooking_time'] = recipe.cooking_time
        return data


class IsInShippingCartSerializer(serializers.ModelSerializer):

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
        data['image'] = recipe.image
        data['cooking_time'] = recipe.cooking_time
        return data
