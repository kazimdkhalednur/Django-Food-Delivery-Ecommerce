from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path("", views.OrderAPIView.as_view(), name="order"),
    path("payment/", csrf_exempt(views.CreateCheckOutSession.as_view()), name="payment"),
    path("hook/", views.stripe_webhook_view, name="payment"),
]
