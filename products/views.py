from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Food, Category
from .serializers import FoodDetailSerializer, FoodCreateSerializer
from accounts.models import User


class FoodAPIView(APIView):
    def get(self, request, format=None):
        food_list = Food.objects.all()
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


class CheckAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({"msg": "ok"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
