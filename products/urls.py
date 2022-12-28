from django.urls import path
from . import views


app_name = 'food'
urlpatterns = [
    path('', views.FoodAPIView.as_view(), name='list'),
    path('check/', views.CheckAPIView.as_view(), name='check'),
    path('category/', views.CategoryAPIView.as_view(), name='category'),
    path('<pk>/', views.FoodDetailAPIView.as_view(), name='detail'),
]
