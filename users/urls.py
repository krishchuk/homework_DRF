from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

from users.apps import UsersConfig
from users.views import UserViewSet, PayListAPIView, PayCreateAPIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register('', UserViewSet, basename='user')
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(permission_classes=[AllowAny]), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=[AllowAny]), name='token_refresh'),

    path('pays/', PayListAPIView.as_view(), name='pay_list'),
    path('pay/', PayCreateAPIView.as_view(), name='payment')
] + router.urls
