from django.urls import path
from . import views


app_name = 'food'
urlpatterns = [
    path('', views.FoodAPIView.as_view()),
    path('seller/', views.SellerFoodAPIVIew.as_view()),
    path('seller/food/status/<pk>/', views.FoodStatusAPIView.as_view()),
    path('seller/food/<pk>/', views.FoodDetailAPIView.as_view()),
    path('check/', views.CheckAPIView.as_view()),
    path('category/', views.CategoriesAPIView.as_view()),
    path('seller/category/', views.SellerCategoriesAPIView.as_view()),
    path('seller/category/status/<pk>/', views.CategoryStatusAPIView.as_view()),
    path('seller/<category>/', views.FoodListByCategoryAPIView.as_view()),
    path('category/create/', views.CreateCategoryAPIView.as_view()),
    path('category/<pk>/', views.CategoryAPIView.as_view()),
    path('<pk>/', views.FoodDetailAPIView.as_view()),
]
