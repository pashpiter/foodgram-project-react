from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from .models import Subscribe, User
from .serializers import IsSubscribedSeializer, UserRegistrationSerializer


class UserCreateGetPatchViewSet(UserViewSet):
    """ViewSet для создания User"""
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        if 'role' not in self.request.data:
            serializer.save(role='user')


class SubscribeViewSet(viewsets.ModelViewSet):
    """ViewSet для создания подписок"""
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
    """ViewSet для получения подписок"""
    queryset = Subscribe.objects.all()
    serializer_class = IsSubscribedSeializer
