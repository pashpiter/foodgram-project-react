from django.urls import include, path
from djoser.views import TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import (APIDestroyTokenView, APIGetTokenView, GetSubscriptionsView,
                    SubscribeViewSet, UserCreateGetPatchViewSet)

router = DefaultRouter()
router.register('users', UserCreateGetPatchViewSet, basename='users')

urlpatterns = [
    path(
        'users/<author_id>/subscribe',
        SubscribeViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
        name='subscribe'
    ),
    path(
        'users/subscriptions',
        GetSubscriptionsView.as_view({'get': 'list'}),
        name='getsubs'
    ),
    path('', include(router.urls)),
    path('auth/token/login', APIGetTokenView.as_view(), name='get_token'),
    path(
        'auth/token/logout', TokenDestroyView.as_view(), name='token_destroy'
    ),
    path(
        'auth/token/logout',
        APIDestroyTokenView.as_view(),
        name='token_destroy'),
]
