from rest_framework import serializers
from .models import Food, Category


class FoodDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'title', 'price', 'image', 'description', 'category')
        depth = 1


class FoodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('title', 'price', 'description', 'category')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
