from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, IngridientViewSet, RecipeViewSet, FavoriteViewSet, IsInShippingCartViewSet


router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingridients', IngridientViewSet, basename='ingridients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
    'recipes/<recipe_id>/favorite',
    FavoriteViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
    name='isfavorite'),
    path('recipes/<recipe_id>/shopping_cart',
         IsInShippingCartViewSet.as_view({
            'post': 'create', 'delete': 'destroy'
         })),
    path('', include(router.urls))
]