from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.models import User, Pay


class PaySerializer(serializers.ModelSerializer):
    user = SerializerMethodField()

    def get_user(self, obj):
        return int(self.context.get('request', None).user.id)

    class Meta:
        model = Pay
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    pay_history = PaySerializer(source='pay_set', many=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'city', 'avatar', 'pay_history', 'password',)


class OtherUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'phone', 'city', 'avatar',)
