from django.urls import path
from . import views


app_name = 'food'
urlpatterns = [
    path('', views.FoodAPIView.as_view(), name='list'),
    path('seller/', views.SellerFoodAPIVIew.as_view(), name='all'),
    path('seller/food/status/<pk>/',
         views.FoodStatusAPIView.as_view(), name='status'),
    path('seller/food/<pk>/', views.FoodDetailAPIView.as_view(), name='detail'),
    path('check/', views.CheckAPIView.as_view(), name='check'),
    path('category/', views.CategoriesAPIView.as_view(), name='category'),
    path('seller/category/', views.SellerCategoriesAPIView.as_view(),
         name='seller-category'),
    path('seller/category/status/<pk>/',
         views.CategoryStatusAPIView.as_view(), name='category-status'),
    path('category/create/', views.CreateCategoryAPIView.as_view(),
         name='create-category'),
    path('category/<pk>/', views.CategoryAPIView.as_view(), name='category'),
    path('<pk>/', views.FoodDetailAPIView.as_view(), name='detail'),
]
