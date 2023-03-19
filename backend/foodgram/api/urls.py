from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, IngridientViewSet, RecipeViewSet


router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingridients', IngridientViewSet, basename='ingridients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls))
]