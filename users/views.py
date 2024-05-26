from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import User, Pay
from users.serializers import UserSerializer, PaySerializer, OtherUserSerializer
from users.services import create_stripe_price, create_stripe_session, create_stripe_product


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return OtherUserSerializer
    #     elif self.action in ['update', 'retrieve']:
    #         for obj in self.queryset:
    #             if obj.id == self.request.user.id:
    #                 return UserSerializer
    #         return OtherUserSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PayListAPIView(ListAPIView):
    serializer_class = PaySerializer
    queryset = Pay.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('payment_method', 'paid_course', 'paid_lesson')
    ordering_fields = ('pay_date',)


class PayCreateAPIView(CreateAPIView):
    serializer_class = PaySerializer
    queryset = Pay.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.user = self.request.user
        if self.request.paid_course:
            product = create_stripe_product(self.request.paid_course)
        else:
            product = create_stripe_product(self.request.paid_lesson)
        stripe_price = create_stripe_price(payment.payment_amount, product)
        session_id, payment_link = create_stripe_session(stripe_price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
