from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import Subscribe, User


class UserRegistrationSerializer(UserCreateSerializer):
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


class IsSubscribedSeializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=UserRegistrationSerializer(), required=False
    )
    subscriber = serializers.HiddenField(default=False)

    class Meta:
        model = Subscribe
        fields = ('author', 'subscriber')

    def to_representation(self, instance):
        data = super(IsSubscribedSeializer, self).to_representation(
            instance.author)
        data['id'] = instance.author.id
        data['username'] = instance.author.username
        data['email'] = instance.author.email
        data['first_name'] = instance.author.first_name
        data['last_name'] = instance.author.last_name
        data['is_subscribed'] = True
        return data
