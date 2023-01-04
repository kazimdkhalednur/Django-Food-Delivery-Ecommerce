import stripe
from decimal import Decimal
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from .models import Cart, Order
from products.models import Food
from .serializers import OrderSerializer, ReviewSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderAPIView(APIView):
    def post(self, request, format=None):
        if request.user.is_authenticated:
            if request.user.type == "buyer":
                if request.data:
                    order = Order.objects.create(
                        user=request.user,
                        address=request.data['address'],
                        phone=request.data['phone'],
                        status='pending'
                    )
                    amount = 0
                    for cart in request.data['cart']:
                        food = Food.objects.get(id=cart['id'])
                        amount += (cart['quantity'] * food.price)
                        cart_obj = Cart.objects.create(
                            user=request.user, food=food, quantity=cart['quantity'])
                        order.cart.add(cart_obj)
                        order.save()
                    order.amount = Decimal(amount)
                    order.save()
                    return Response({"msg": "Order created successfully", "id": order.id}, status=status.HTTP_201_CREATED)
                return Response({"msg": "error"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CreateCheckOutSession(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.type == "buyer":
                id = request.data['id']
                try:
                    order = Order.objects.get(id=id, user=request.user)
                    checkout_session = stripe.checkout.Session.create(
                        line_items=[
                            {
                                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                                'price_data': {
                                    'currency': 'usd',
                                    'unit_amount': int(order.amount) * 100,
                                    'product_data': {
                                        'name': 'Total amount'
                                    }
                                },
                                'quantity': 1,
                            },
                        ],
                        metadata={
                            "order_id": order.id
                        },
                        mode='payment',
                        success_url=settings.SITE_URL + 'order?success=true',
                        cancel_url=settings.SITE_URL + '?canceled=true',
                    )
                    order.pending_payment_url = checkout_session.url
                    order.save()
                    return Response(checkout_session, status=200)
                except Exception as e:
                    return Response({'msg': 'something went wrong while creating stripe session', 'error': str(e)}, status=500)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_SECRET_WEBHOOK
        )
    except ValueError as e:
        # Invalid payload
        return Response(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return Response(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        print(session)
        id = session['metadata']['order_id']
        order = Order.objects.get(id=id)
        if session['payment_status']:
            order.txnid = session['payment_intent']
            order.is_paid = True
            order.status = 'paid'
            order.is_ordered = True
        else:
            order.status = 'stole'
        order.save()

    return HttpResponse(status=200)


class OrderListAPIView(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            if request.user.type == "buyer":
                order_list = Order.objects.filter(
                    user=request.user).exclude(status="stolen").order_by('-created_at')
                serializer = OrderSerializer(order_list, many=True)

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class SellerOrderListAPIView(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                query = Q() | Q(status="pending") | Q(status="stolen")
                order_list = Order.objects.exclude(
                    query).order_by('-created_at')
                serializer = OrderSerializer(order_list, many=True)

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class PendingOrderListAPIView(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                order_list = Order.objects.filter(
                    status="paid").order_by('-created_at')
                serializer = OrderSerializer(order_list, many=True)

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ReviewAPIView(APIView):
    def get(self, request, pk, format=None):
        food = Food.objects.get(id=pk)
        cart_list = Cart.objects.filter(food=food).order_by('-created_at')
        review = []
        for cart in cart_list:
            for order in cart.order_set.all().order_by('-created_at'):
                if order.status == "delivered" and (cart.review or cart.rating):
                    review.append({
                        "name": cart.user.full_name,
                        "review": cart.review,
                        "rating": cart.rating
                    })
        return Response(review, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.type == "buyer":
                if request.data:
                    rating = request.data['rating']
                    review = request.data['review']
                    food = Food.objects.get(id=pk)
                    order_list = Order.objects.filter(
                        user=request.user, status="delivered").order_by("-created_at")
                    for cart in order_list[0].cart.all():
                        if cart.food.id == food.id:
                            cart.rating = rating
                            cart.review = review
                            cart.save()
                    return Response({"msg": "success"}, status=status.HTTP_201_CREATED)
                return Response({"msg": "error"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserReviewAPIView(APIView):
    def get(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.type == "buyer":
                food = Food.objects.get(id=pk)
                order_list = Order.objects.filter(
                    user=request.user, status="delivered").order_by("-created_at")
                for cart in order_list[0].cart.all():
                    if cart.food.id == food.id:
                        if cart.review or cart.rating:
                            return Response({"msg": False}, status=status.HTTP_200_OK)
                        return Response({"msg": True}, status=status.HTTP_200_OK)
                return Response({"msg": False}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
