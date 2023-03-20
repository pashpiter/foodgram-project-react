from rest_framework import serializers
from django.shortcuts import get_object_or_404

from recipes.models import Tag, Ingridient, RecipeList, IsFavorited, IsInShippingCart, IngridientInRecipe


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug')


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
    ingridients = IngridientsInRecipeSerializer(many=True)

    class Meta:
        model = RecipeList
        fields = (
            'id', 'tags', 'author', 'ingridients', 'is_favorited',
            'is_in_shipping_cart', 'name', 'image', 'text', 'cooking_time')
        read_only_fields = ('author', 'is_favorited', 'is_in_shipping_cart')
        
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
    
    
    