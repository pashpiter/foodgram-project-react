from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes

from recipes.models import Tag, Ingridient, RecipeList
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import TagSerializer, IngridientsSerializer, RecipeSerializer
from .permissions import IsAuthorOrModeratorOrAdminOrReadOnly, IsAdmin


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
