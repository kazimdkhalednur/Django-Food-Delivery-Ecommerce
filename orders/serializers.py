from rest_framework import serializers
from .models import Cart, Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "pending_payment_url", "cart",
                  "status", "order_id", "amount", "address", "deliver_user")
        depth = 2


class SellerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "address", "")


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ("review", "rating", "user")
        depth = 1


class DeliverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "order_id", "deliver_user")
        depth = 1


class CreateDeliverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "order_id", "deliver_user")


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "order_id", "status")
