from django.urls import path
from . import views


app_name = 'food'
urlpatterns = [
    path('', views.FoodAPIView.as_view(), name='list'),
    path('check/', views.CheckAPIView.as_view(), name='check'),
    path('category/', views.CategoriesAPIView.as_view(), name='category'),
    path('category/create/', views.CreateCategoryAPIView.as_view(),
         name='create-category'),
    path('category/<pk>/', views.CategoryAPIView.as_view(), name='category'),
    path('<pk>/', views.FoodDetailAPIView.as_view(), name='detail'),
]
