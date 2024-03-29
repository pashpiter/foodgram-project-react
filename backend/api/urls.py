from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShippingCartViewSet, FavoriteViewSet,
                    IngredientViewSet, IsInShippingCartViewSet, RecipeViewSet,
                    TagViewSet)

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        'recipes/<recipe_id>/favorite/',
        FavoriteViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
        name='isfavorite'),
    path('recipes/<recipe_id>/shopping_cart/',
         IsInShippingCartViewSet.as_view({
             'post': 'create', 'delete': 'destroy'
         }), name='shopping_cart'),
    path('recipes/download_shopping_cart/',
         DownloadShippingCartViewSet.as_view({'get': 'list'}),
         name='download_shopping_cart'),
    path('', include(router.urls))
]
