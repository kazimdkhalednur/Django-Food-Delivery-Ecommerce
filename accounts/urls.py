from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from . import views

urlpatterns = [
    path('registration/', views.SignUpView.as_view()),
    path('login/', views.UserTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('detail/', views.UserDetailView.as_view()),
    path('deliver/', views.DeliveryManAPIView.as_view()),
    path('seller/list/', views.SellerListAPIView.as_view()),
    path('buyer/list/', views.BuyerListAPIView.as_view()),
    path('deliver/list/', views.DeliveryManListAPIView.as_view()),
    path('active/<pk>/', views.UserActiveAPIView.as_view()),
    path('detail/<pk>/', views.RetrieveUpdateDeleteUserAPIView.as_view()),
    path('create/', views.UserCreateAPIView.as_view()),
]
