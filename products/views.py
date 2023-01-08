from asd import asd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Food, Category
from .serializers import FoodSerializer, FoodCreateSerializer, CategorySerializer, CreateCategorySerializer
from accounts.models import User


class FoodAPIView(APIView):
    def get(self, request, format=None):
        food_list = Food.objects.filter(is_visible=True)
        serializer = FoodSerializer(food_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SellerFoodAPIVIew(APIView):
    def get(self, request, format=None):
        food_list = Food.objects.all().order_by("-created_at")
        serializer = FoodSerializer(food_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                serializer = FoodCreateSerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save(user=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class FoodDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        food = self.get_object(pk)
        serializer = FoodSerializer(food)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        food_obj = Food.objects.get(id=pk)
        serializer = FoodSerializer(food_obj, data=request.data, partial=True)
        if serializer.is_valid():
            if food_obj.user == request.user:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if (Food.objects.filter(id=pk)).exists():
            serializer_del = Food.objects.get(id=pk)
            if serializer_del.user == request.user:
                serializer_del.delete()
                return Response({"msg": "delete Successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class FoodStatusAPIView(APIView):
    def get_object(self, pk):
        try:
            return Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                food = self.get_object(pk)
                if food.is_visible:
                    food.is_visible = False
                    food.save()
                    return Response({"msg": "Public"}, status=status.HTTP_200_OK)
                else:
                    food.is_visible = True
                    food.save()
                    return Response({"msg": "Hide"}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CategoriesAPIView(APIView):
    def get(self, request, format=None):
        category_list = Category.objects.filter(is_visible=True)
        serializer = CategorySerializer(category_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SellerCategoriesAPIView(APIView):
    def get(self, request, format=None):
        category_list = Category.objects.all()
        serializer = CategorySerializer(category_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateCategoryAPIView(APIView):
    def post(self, request, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                serializer = CreateCategorySerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CategoryAPIView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                category = self.get_object(pk)
                serializer = CreateCategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                category = self.get_object(pk)
                serializer = CreateCategorySerializer(
                    category, data=request.data, partial=True)
                if serializer.is_valid():
                    print(request.data)
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                category = self.get_object(pk)
                category.delete()
                return Response({"msg": "delete Successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CategoryStatusAPIView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                category = self.get_object(pk)
                if category.food_set.all().exists():
                    for food in category.food_set.all():
                        if category.is_visible:
                            category.is_visible = False
                            category.save()
                            food.is_visible = False
                            food.save()
                            return Response({"msg": "Public"}, status=status.HTTP_200_OK)
                        else:
                            category.is_visible = True
                            category.save()
                            food.is_visible = True
                            food.save()
                            return Response({"msg": "Hide"}, status=status.HTTP_200_OK)
                else:
                    if category.is_visible:
                        category.is_visible = False
                        category.save()
                        return Response({"msg": "Public"}, status=status.HTTP_200_OK)
                    else:
                        category.is_visible = True
                        category.save()
                        return Response({"msg": "Hide"}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CheckAPIView(APIView):
    def get(self, request):
        for data in asd:
            category = Category.objects.get(title=data['category'])
            Food.objects.create(user=request.user, title=data['title'], category=category,
                                price=data['price'], description=data['description'])
        if request.user.is_authenticated:
            return Response({"msg": "ok"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        if request.user.is_authenticated:
            print(request.data.get('user'))
            return Response({"msg": "ok"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
