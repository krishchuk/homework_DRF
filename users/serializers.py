from rest_framework import serializers

from users.models import User, Pay


class PaySerializer(serializers.ModelSerializer):
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
