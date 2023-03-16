from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import APIGetTokenView, APIDestroyTokenView, UserCreateGetPatchViewSet, SubscribeViewSet, GetSubscriptionsView
from djoser.views import TokenDestroyView

router = DefaultRouter()
router.register('users', UserCreateGetPatchViewSet, basename='users')
# router.register(r'users/(?P<user_id>\d+)/subscribe', SubscribeViewSet, basename='subscribe')

urlpatterns = [
    path('users/<author_id>/subscribe', SubscribeViewSet.as_view({'post': 'create', 'delete': 'destroy'}), name='subscribe'),
    path('users/subscriptions', GetSubscriptionsView.as_view({'get': 'list'}), name='getsubs'),
    path('', include(router.urls)),
    # path('', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    path('auth/token/login', APIGetTokenView.as_view(), name='get_token'),
    # path('auth/token/logout', TokenDestroyView.as_view(), name='token_destroy'),
    path('auth/token/logout', APIDestroyTokenView.as_view(), name='token_destroy'),
]

