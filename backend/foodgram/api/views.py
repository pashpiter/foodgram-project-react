from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes

from recipes.models import Tag, Ingridient, RecipeList, IsFavorited, IsInShippingCart
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_201_CREATED

from rest_framework.permissions import AllowAny, IsAuthenticated
from user.models import User
from .serializers import TagSerializer, IngridientsSerializer, RecipeSerializer, IsFavoriteSerializer, IsInShippingCartSerializer
from .permissions import IsAuthorOrModeratorOrAdminOrReadOnly, IsAdmin, IsAuthor
from .mixins import CreateDestroyViewSet


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngridientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingridient.objects.all()
    serializer_class = IngridientsSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = RecipeList.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny,]
        elif self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated,]
        elif self.request.method == 'PATCH':
            self.permission_classes = [IsAuthorOrModeratorOrAdminOrReadOnly,]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsAuthorOrModeratorOrAdminOrReadOnly,]
        else:
            self.permission_classes = [IsAuthenticated,]
        return super().get_permissions()


class FavoriteViewSet(CreateDestroyViewSet):
    queryset = IsFavorited.objects.all()
    serializer_class = IsFavoriteSerializer
        
    def create(self, request, *args, **kwargs):
        follower = User.objects.get(id=request.user.id)
        fav_recipe = RecipeList.objects.get(id=self.kwargs['recipe_id'])
        if IsFavorited.objects.filter(fav_recipe_id=self.kwargs['recipe_id'], follower=request.user).exists():
            return Response('Этот рецепт уже в избранном', status=HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, fav_recipe, follower)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer, fav_recipe, follower):
        serializer.save(follower=follower, fav_recipe=fav_recipe)

    def destroy(self, request, *args, **kwargs):
        instance = IsFavorited.objects.filter(fav_recipe_id=self.kwargs['recipe_id'], follower=request.user)
        if not instance.exists():
            return Response('Такого рецепта нет в вашем списке избранного', status=HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response('Вы удалили рецепт из избранного', status=HTTP_204_NO_CONTENT)


class IsInShippingCartViewSet(CreateDestroyViewSet):
    queryset = IsInShippingCart
    serializer_class = IsInShippingCartSerializer

    def create(self, request, *args, **kwargs):
        food_list = RecipeList.objects.get(id=self.kwargs['recipe_id'])
        user_cart = User.objects.get(id=request.user.id)
        if IsInShippingCart.objects.filter(food_list_id=self.kwargs['recipe_id'], user_cart=request.user).exists():
            return Response('Этот рецепт уже в корзине', status=HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, food_list, user_cart)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer, food_list, user_cart):
        serializer.save(food_list=food_list, user_cart=user_cart)
    
    def destroy(self, request, *args, **kwargs):
        instance = IsInShippingCart.objects.filter(food_list=self.kwargs['recipe_id'], user_cart=request.user)
        if not instance.exists():
            return Response('Такого рецепта нет в вашей корзине', status=HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response('Вы удалили рецепт из корзины', status=HTTP_204_NO_CONTENT)
    
class DownloadShippingCartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IsInShippingCart
    permission_classes = IsAuthor

    def list(self, request, *args, **kwargs):
        pass