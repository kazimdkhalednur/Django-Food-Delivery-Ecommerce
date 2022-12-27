from decimal import Decimal
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Cart, Order
from accounts.models import User
from .serializers import CartSerializer, OrderSerializer


class CartAPIView(APIView):
    def post(self, request, format=None):
        if request.user.is_authenticated:
            if request.user.type == "buyer":
                serializer = CartSerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save(user=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class OrderAPIView(APIView):
    def post(self, request, format=None):
        if request.user.is_authenticated:
            if request.user.type == "buyer":
                serializer = OrderSerializer(data=request.data)

                if serializer.is_valid():
                    # for cart in serializer.cart.all():
                    #     print(cart.food.title)
                    # serializer.amount = Decimal(123.678)
                    serializer.save(user=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
