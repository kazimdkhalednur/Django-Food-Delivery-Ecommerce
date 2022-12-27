from rest_framework import serializers
from .models import Cart, Order


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('food', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('cart', 'amount')
