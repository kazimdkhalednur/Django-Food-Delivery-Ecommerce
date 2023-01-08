from rest_framework import serializers
from .models import Food, Category


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'title', 'price', 'image',
                  'description', 'category', 'is_visible')
        depth = 1


class FoodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('title', 'price', 'description', 'category', 'image')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title", "image")
