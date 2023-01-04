from rest_framework import serializers
from .models import Cart, Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "pending_payment_url", "cart",
                  "status", "order_id", "amount", "address")
        depth = 2


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ("review", "rating", "user")
        depth = 1
