from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PayListAPIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register('', UserViewSet, basename='user')
urlpatterns = [
    path('pay/', PayListAPIView.as_view(), name='pay_list'),
] + router.urls
