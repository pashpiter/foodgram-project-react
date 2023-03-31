from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from recipes.models import (Ingredient, IngredientInRecipe, IsFavorited,
                            IsInShippingCart, RecipeList, Tag)
from user.models import User

from .mixins import CreateDestroyViewSet
from .filters import TagAuthorFavoriteCartFilter
from .serializers import (IngredientsSerializer, IsFavoriteSerializer,
                          IsInShippingCartSerializer, RecipeSerializer,
                          TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для тегов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для ингредиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None

    def get_queryset(self):
        name = self.request.query_params['name']
        name = name.lower()
        starts_with_queryset = list(
            self.queryset.filter(name__istartswith=name)
        )
        cont_queryset = self.queryset.filter(name__icontains=name)
        starts_with_queryset.extend(
            [ing for ing in cont_queryset if ing not in starts_with_queryset]
        )
        return starts_with_queryset


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для рецептов"""
    queryset = RecipeList.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TagAuthorFavoriteCartFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteViewSet(CreateDestroyViewSet):
    """ViewSet для избранного"""
    queryset = IsFavorited.objects.all()
    serializer_class = IsFavoriteSerializer

    def create(self, request, *args, **kwargs):
        follower = User.objects.get(id=request.user.id)
        fav_recipe = RecipeList.objects.get(id=self.kwargs['recipe_id'])
        if IsFavorited.objects.filter(
            fav_recipe_id=self.kwargs['recipe_id'], follower=request.user
        ).exists():
            return Response(
                'Этот рецепт уже в избранном', status=HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, fav_recipe, follower)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer, fav_recipe, follower):
        serializer.save(follower=follower, fav_recipe=fav_recipe)

    def destroy(self, request, *args, **kwargs):
        instance = IsFavorited.objects.filter(
            fav_recipe_id=self.kwargs['recipe_id'], follower=request.user
        )
        if not instance.exists():
            return Response(
                'Такого рецепта нет в вашем списке избранного',
                status=HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(
            'Вы удалили рецепт из избранного', status=HTTP_204_NO_CONTENT
        )


class IsInShippingCartViewSet(CreateDestroyViewSet):
    """ViewSet для корзины"""
    queryset = IsInShippingCart
    serializer_class = IsInShippingCartSerializer

    def create(self, request, *args, **kwargs):
        food_list = RecipeList.objects.get(id=self.kwargs['recipe_id'])
        user_cart = User.objects.get(id=request.user.id)
        if IsInShippingCart.objects.filter(
            food_list_id=self.kwargs['recipe_id'], user_cart=request.user
        ).exists():
            return Response(
                'Этот рецепт уже в корзине', status=HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, food_list, user_cart)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer, food_list, user_cart):
        serializer.save(food_list=food_list, user_cart=user_cart)

    def destroy(self, request, *args, **kwargs):
        instance = IsInShippingCart.objects.filter(
            food_list=self.kwargs['recipe_id'], user_cart=request.user
        )
        if not instance.exists():
            return Response(
                'Такого рецепта нет в вашей корзине',
                status=HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(
            'Вы удалили рецепт из корзины', status=HTTP_204_NO_CONTENT
        )


class DownloadShippingCartViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для загрузки ингредиентов"""
    queryset = IsInShippingCart

    def list(self, request, *args, **kwargs):
        recipes = IsInShippingCart.objects.filter(user_cart_id=request.user.id)
        end_ingredients = {}
        for recipe in recipes:
            ingredients = IngredientInRecipe.objects.filter(
                recipe=recipe.food_list
            )
            for ingredient in ingredients:
                if ingredient.ingredient_in_recipe.id not in end_ingredients:
                    end_ingredients[
                        ingredient.ingredient_in_recipe.id] = ingredient
                else:
                    end_ingredients[
                        ingredient.ingredient_in_recipe.id
                    ].amount += ingredient.amount
        shopping_list = ''
        for ingredient in end_ingredients.values():
            item = (''.join(
                f'{ingredient.ingredient_in_recipe.name} '
                f'({ingredient.ingredient_in_recipe.measurement_unit}) - '
                f'{ingredient.amount}\n'
            ))
            shopping_list += item
        return HttpResponse(
            shopping_list, content_type='text/plain;charset=UTF-8'
        )
