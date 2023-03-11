from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.decorators import action

from .serializers import UserRegistrationSerializer, UserGetSerializer
from .models import User
from api.permissions import IsAdminOrReadOnly, IsAdmin
from rest_framework.permissions import AllowAny


class UserCreateGetPatchViewSet(UserViewSet):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)

    def perform_create(self, serializer):
        if 'role' not in self.request.data:
            serializer.save(role='user')
        serializer.save()
