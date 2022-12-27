from django.urls import path
from . import views

urlpatterns = [
    path("", views.OrderAPIView.as_view(), name="order"),
    path("cart/", views.CartAPIView.as_view(), name="cart"),
]
