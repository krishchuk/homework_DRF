from rest_framework import serializers

from users.models import User, Pay


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'city', 'avatar', 'password',)


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = '__all__'
