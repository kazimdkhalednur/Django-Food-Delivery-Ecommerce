from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer

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

