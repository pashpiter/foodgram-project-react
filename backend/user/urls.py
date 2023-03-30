from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (SubscriptionsViweSet,
                    UserCreateGetPatchViewSet)

router = DefaultRouter()
router.register('users', UserCreateGetPatchViewSet, basename='users')

urlpatterns = [
    path(
        'users/<author_id>/subscribe/',
        SubscriptionsViweSet.as_view({'post': 'create', 'delete': 'destroy'}),
        name='subscribe'
    ),
    path(
        'users/subscriptions/',
        SubscriptionsViweSet.as_view({'get': 'list'}),
        name='getsubs'
    ),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
