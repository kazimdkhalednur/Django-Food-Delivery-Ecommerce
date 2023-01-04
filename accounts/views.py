from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User
from .serializers import UserSerializer, UserDetailSerializer, UserTokenObtainPairSerializer


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
