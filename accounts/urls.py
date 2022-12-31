from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from . import views

urlpatterns = [
    path('registration/', views.SignUpView.as_view(), name='registration'),
    path('login/', views.UserTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('detail/', views.UserDetailView.as_view(), name='user-detail'),
]
