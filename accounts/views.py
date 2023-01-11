from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User
from .serializers import *


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        if User.objects.filter(email=request.data["email"]):
            return Response({"detail": "Email Already Exist"}, status=status.HTTP_306_RESERVED)

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


class UserDetailView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            user_serializer = UserDetailSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        if request.user.is_authenticated:
            print(request.data)
            user = User.objects.get(id=request.user.id)
            user_serializer = UserDetailSerializer(
                user, data=request.data, partial=True)
            print(user_serializer)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeliveryManAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                user = User.objects.filter(type="deliver")
                user_serializer = DeliverUserSerializer(user, many=True)
                return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class SellerListAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                user = User.objects.filter(type="seller")
                user_serializer = UserListSerializer(user, many=True)
                return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                user = User.objects.get(id=request.data['id'])
                user.delete()
                return Response({"msg": "delete Successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class BuyerListAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                user = User.objects.filter(type="buyer")
                user_serializer = UserListSerializer(user, many=True)
                return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeliveryManListAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                user = User.objects.filter(type="deliver")
                user_serializer = UserListSerializer(user, many=True)
                return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RetrieveUpdateDeleteUserAPIView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                user = self.get_object(pk=pk)
                serializer = UserFullDetailSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                user = self.get_object(pk=pk)
                serializer = UserDetailSerializer(
                    user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                user = self.get_object(pk=pk)
                user.delete()
                return Response({"msg": "delete Successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserActiveAPIView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                user = self.get_object(pk=pk)
                if user.is_active:
                    user.is_active = False
                    user.save()
                    return Response({"active": False}, status=status.HTTP_200_OK)
                else:
                    user.is_active = True
                    user.save()
                    return Response({"active": True}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserCreateAPIView(APIView):
    def post(self, request, format=None):
        if request.user.is_authenticated:
            serializer = UserCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
