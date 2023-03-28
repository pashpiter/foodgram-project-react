from django.http import FileResponse
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from recipes.models import (Ingridient, IngridientInRecipe, IsFavorited,
                            IsInShippingCart, RecipeList, Tag)
from user.models import User

from .mixins import CreateDestroyViewSet
from .permissions import IsAuthor, IsAuthorOrAdminOrReadOnly
from .serializers import (IngridientsSerializer, IsFavoriteSerializer,
                          IsInShippingCartSerializer, RecipeSerializer,
                          TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngridientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingridient.objects.all()
    serializer_class = IngridientsSerializer
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
    queryset = RecipeList.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        queryset = self.queryset
        tags = self.request.query_params.get('tags')
        if tags:
            queryset = queryset.filter(tags__slug=tags).distinct()
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author__username=author)
        if not self.request._user.is_authenticated:
            return queryset

        if self.request.query_params.get('is_favorited'):
            queryset = queryset.filter(follower__user=self.request.user)
        if not self.request.query_params.get('is_in_cart'):
            return queryset
        return queryset.filter(user_cart__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        elif self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, ]
        elif self.request.method == 'PATCH':
            self.permission_classes = [IsAuthorOrAdminOrReadOnly, ]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsAuthorOrAdminOrReadOnly, ]
        else:
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()


class FavoriteViewSet(CreateDestroyViewSet):
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
    queryset = IsInShippingCart
    permission_classes = [IsAuthor, ]

    def list(self, request, *args, **kwargs):
        recipes = IsInShippingCart.objects.filter(user_cart_id=request.user.id)
        end_ingridients = {}
        for recipe in recipes:
            ingridients = IngridientInRecipe.objects.filter(
                recipe_id=recipe.food_list_id
            )
            for ingridient in ingridients:
                if ingridient.ingridient_in_recipe.id not in end_ingridients:
                    end_ingridients[
                        ingridient.ingridient_in_recipe.id] = ingridient
                else:
                    end_ingridients[
                        ingridient.ingridient_in_recipe.id
                    ].amount += ingridient.amount
        file = open("shopping_list.txt", "w+")
        for ingridient in end_ingridients.values():
            file.write(''.join(
                f'{ingridient.ingridient_in_recipe.name} '
                f'({ingridient.ingridient_in_recipe.measurement_unit}) - '
                f'{ingridient.amount}\n'
            ))
        return FileResponse(
            file, as_attachment=True, filename='shopping_list.txt'
        )
