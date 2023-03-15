from djoser.views import UserViewSet, TokenDestroyView
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password, make_password, is_password_usable
from djoser.conf import settings
from django.contrib.auth import logout

from .utils import create_jwt_token
from .serializers import (
    UserRegistrationSerializer, UserSetPasswoprdSerializer, GetTokenSerializer
)
from .models import User
from .permissions import IsMe
from rest_framework.permissions import AllowAny


class APIDestroyTokenView(APIView):

    def post(self, request):
        print(request.auth.token)
        # print(request.user._auth.token)
        request.auth.delete()
        return Response(status=HTTP_200_OK)

class APIGetTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = get_object_or_404(User, email=email)
        if not check_password(password, user.password):
            return Response('Неверный пароль или почта', status=HTTP_400_BAD_REQUEST)
        return Response({'auth_token': create_jwt_token(user)})


class UserCreateGetPatchViewSet(UserViewSet):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        if 'role' not in self.request.data:
            serializer.save(role='user')
        print(self.request.data)
        password = make_password(self.request.data.get('password'))
        serializer.save(password=password)
    
    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        serializer = UserSetPasswoprdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']
        current_password = serializer.validated_data['current_password']
        user = get_object_or_404(User, username=request.user)
        if not check_password(current_password, user.password):
            return Response('Существующий пароль не совпадает', status=HTTP_400_BAD_REQUEST)
        if current_password == new_password:
            return Response('Новый пароль совпадает со старым', status=HTTP_400_BAD_REQUEST)
        user.password = make_password(new_password)
        user.save()
        return Response('Пароль изменен', status=HTTP_200_OK)

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset