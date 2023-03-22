from django.contrib.auth.hashers import (check_password, make_password)
from django.shortcuts import get_object_or_404
from djoser.views import TokenDestroyView, UserViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView

from .models import Subscribe, User
from .serializers import (GetTokenSerializer, IsSubscribedSeializer,
                          UserRegistrationSerializer,
                          UserSetPasswoprdSerializer)
from .utils import create_jwt_token


class APIDestroyTokenView(TokenDestroyView):

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
            return Response(
                'Неверный пароль или почта',
                status=HTTP_400_BAD_REQUEST
            )
        return Response({'auth_token': create_jwt_token(user)})


class UserCreateGetPatchViewSet(UserViewSet):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        if 'role' not in self.request.data:
            serializer.save(role='user')
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
            return Response(
                'Существующий пароль не совпадает',
                status=HTTP_400_BAD_REQUEST
            )
        if current_password == new_password:
            return Response(
                'Новый пароль совпадает со старым',
                status=HTTP_400_BAD_REQUEST
            )
        user.password = make_password(new_password)
        user.save()
        return Response('Пароль изменен', status=HTTP_200_OK)

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class SubscribeViewSet(viewsets.ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = IsSubscribedSeializer
    http_method_names = ['post', 'delete']

    def create(self, request, *args, **kwargs):
        subscriber = get_object_or_404(User, pk=request.user.id)
        author = get_object_or_404(User, pk=self.kwargs['author_id'])
        if subscriber == author:
            return Response(
                'Вы не можете подписаться на самого себя',
                status=HTTP_400_BAD_REQUEST
            )
        if Subscribe.objects.filter(
            author_id=self.kwargs['author_id'], subscriber=request.user
        ):
            return Response(
                'Вы уже подписаны на этого автора',
                status=HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, subscriber, author)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer, subscriber, author):
        serializer.save(subscriber=subscriber, author=author)

    def destroy(self, request, *args, **kwargs):
        instance = Subscribe.objects.filter(
            author_id=self.kwargs['author_id'], subscriber=request.user
        )
        if not instance.exists():
            return Response(
                'Вы не подписаны на этого автора', status=HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response('Вы отписались', status=HTTP_204_NO_CONTENT)


class GetSubscriptionsView(viewsets.ReadOnlyModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = IsSubscribedSeializer
