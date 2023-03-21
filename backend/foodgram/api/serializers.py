from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.db.models import F

from recipes.models import Tag, Ingridient, RecipeList, IsFavorited, IsInShippingCart, IngridientInRecipe
from user.serializers import UserRegistrationSerializer
from .permissions import IsAdmin
from .utils import UpdateIngridientsInRecipe


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id' ,'name', 'color', 'slug')


class IngridientsInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngridientInRecipe
        fields = ('__all__')
        read_only_fields = ('recipe', 'ingridient_in_recipe', 'measurement_unit')


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
            recipe_ingridient = IngridientInRecipe.objects.create(
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
            UpdateIngridientsInRecipe(instance, ingridients)

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
    
    
    