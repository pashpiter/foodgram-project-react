from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (GetSubscriptionsView, SubscribeViewSet,
                    UserCreateGetPatchViewSet)

router = DefaultRouter()
router.register('users', UserCreateGetPatchViewSet, basename='users')

urlpatterns = [
    path(
        'users/<author_id>/subscribe/',
        SubscribeViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
        name='subscribe'
    ),
    path(
        'users/subscriptions/',
        GetSubscriptionsView.as_view({'get': 'list'}),
        name='getsubs'
    ),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
