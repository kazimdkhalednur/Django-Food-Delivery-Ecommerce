from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path("", views.OrderAPIView.as_view(), name="order"),
    path("list/", views.OrderListAPIView.as_view(), name="order-list"),
    path("seller/list/", views.SellerOrderListAPIView.as_view(),
         name="seller-order-list"),
    path("pending/list/", views.PendingOrderListAPIView.as_view(),
         name="seller-order-list"),
    path("payment/", csrf_exempt(views.CreateCheckOutSession.as_view()), name="payment"),
    path("hook/", views.stripe_webhook_view, name="payment"),
    path('review/<pk>/', views.ReviewAPIView.as_view(), name='review'),
    path('check-review/<pk>/', views.UserReviewAPIView.as_view(), name='review'),
]
