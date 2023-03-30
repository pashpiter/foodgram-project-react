from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import RecipeList

from .models import Subscribe, User


class UserRegistrationSerializer(UserCreateSerializer):
    """Сериализатор для регистрации User"""
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name',
            'last_name', 'password')

    def validate(self, data):
        if not data.get('username'):
            raise ValueError('Необходимо ввести username!')
        if not data.get('first_name'):
            raise ValueError('Необходимо ввести first_name!')
        if not data.get('last_name'):
            raise ValueError('Необходимо ввести last_name!')
        return data


class UserGetSerializer(UserSerializer):
    """Сериализатор для получения объекта User"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name',
            'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        author = Subscribe.objects.filter(author=obj)
        if not author:
            return False
        sub = self.context['request'].user
        return author.filter(subscriber=sub).exists()


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = RecipeList
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSeializer(serializers.ModelSerializer):
    """Сериализатор для подписок"""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('username', 'email', 'first_name', 'last_name',)

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return RecipeList.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        recipes = RecipeList.objects.filter(author=obj)
        return ShortRecipeSerializer(recipes, many=True).data

    def create(self, validated_data):
        subscriber = validated_data.get('subscriber')
        author = validated_data.get('author')
        return Subscribe.objects.create(subscriber=subscriber, author=author)
