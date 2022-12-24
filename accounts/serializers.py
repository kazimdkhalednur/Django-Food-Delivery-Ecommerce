from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "email", "phone", "password", "type")

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        phone = validated_data.pop('phone')
        type = validated_data.pop('type')

        user = User.objects.create_user(
            full_name=full_name, email=email, phone=phone, password=password, type=type)

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "email", "address", "phone")
