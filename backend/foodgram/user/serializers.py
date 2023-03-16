from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from django.shortcuts import get_object_or_404


from .models import User, Subscribe
from .validators import validate_new_password

class GetTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password')


class UserRegistrationSerializer(UserCreateSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_subscribed')

    def get_is_subscribed(self, obj):
        author = Subscribe.objects.filter(author=obj)
        if not author:
            return False
        sub = self.context['request'].user
        return author.filter(subscriber=sub).exists()


class UserSetPasswoprdSerializer(UserSerializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('new_password', 'current_password')

    def validate_new_password(self, value):
        error = validate_new_password(value)
        if error:
            raise serializers.ValidationError(*error)
        return value


class IsSubscribedSeializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=UserRegistrationSerializer(), required=False)
    subscriber = serializers.HiddenField(default=False)

    class Meta:
        model = Subscribe
        fields = ('author', 'subscriber')

    def to_representation(self, instance):
        data = super(IsSubscribedSeializer, self).to_representation(instance.author)
        data['id'] = instance.author.id
        data['username'] = instance.author.username
        data['email'] = instance.author.email
        data['first_name'] = instance.author.first_name
        data['last_name'] = instance.author.last_name
        data['is_subscribed'] = True
        return data
