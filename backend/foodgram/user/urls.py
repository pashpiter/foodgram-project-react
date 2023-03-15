from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import APIGetTokenView, APIDestroyTokenView, UserCreateGetPatchViewSet, SubscribeViewSet
from djoser.views import TokenDestroyView

router = DefaultRouter()
router.register('users', UserCreateGetPatchViewSet)
router.register(r'users/(?P<user_id>\d+)/subscribe', SubscribeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    path('auth/token/login', APIGetTokenView.as_view(), name='get_token'),
    # path('auth/token/logout', TokenDestroyView.as_view(), name='token_destroy'),
    path('auth/token/logout', APIDestroyTokenView.as_view(), name='token_destroy'),
]

