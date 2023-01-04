from asd import asd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Food, Category, Review
from .serializers import FoodDetailSerializer, FoodCreateSerializer, CategorySerializer, CreateCategorySerializer, ReviewSerializer, ReviewCreateSerializer
from accounts.models import User
from orders.models import Order


class FoodAPIView(APIView):
    def get(self, request, format=None):
        food_list = Food.objects.filter(is_visible=True)
        serializer = FoodDetailSerializer(food_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SellerFoodAPIVIew(APIView):
    def get(self, request, format=None):
        food_list = Food.objects.filter(
            is_visible=True).order_by("-created_at")
        serializer = FoodDetailSerializer(food_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                serializer = FoodCreateSerializer(data=request.data)

                if serializer.is_valid():
                    serializer.category = Category.objects.get(
                        id=request.data['category'])
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
        serializer = FoodDetailSerializer(food)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        food_obj = Food.objects.get(id=pk)
        serializer = FoodDetailSerializer(food_obj, data=request.data)
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


class CategoriesAPIView(APIView):
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


class ReviewAPIView(APIView):
    def get(self, request, pk, format=None):
        food = Food.objects.get(id=pk)
        review_list = Review.objects.filter(food=food).order_by('-created_at')
        serializer = ReviewSerializer(review_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if request.user.is_authenticated:
            if request.user.type == "buyer":
                serializer = ReviewCreateSerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save(user=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserReviewAPIView(APIView):
    def get(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.type == "buyer":
                food = Food.objects.get(id=pk)
                order = Order.objects.filter(
                    user=request.user, status="delivered").order_by("-created_at")
                # print(order_list)
                # for order in order_list:
                for cart in order[0].cart.all():
                    print(cart)
                    print(cart.food.id)
                    if cart.food.id == food.id:
                        print("ok")
                    #s     return Response({"msg": "success"}, status=status.HTTP_200_OK)
                    # return Response({"msg": "error"}, status=status.HTTP_200_OK)
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
