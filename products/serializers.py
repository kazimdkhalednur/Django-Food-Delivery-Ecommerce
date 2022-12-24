from rest_framework import serializers
from .models import Food


class FoodDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'title', 'price', 'discount_price',
                  'image', 'description', 'category')
        depth = 1


class FoodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('title', 'price', 'discount_price',
                  'description', 'category')
