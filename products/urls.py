from django.urls import path
from . import views


app_name = 'food'
urlpatterns = [
    path('', views.FoodAPIView.as_view(), name='list'),
    path('<pk>/', views.FoodDetailAPIView.as_view(), name='detail'),
]