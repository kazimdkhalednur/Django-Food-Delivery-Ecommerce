from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from .models import Cart, Order
from products.models import Food
from .serializers import *

SSLCOMMERZE_STORE_ID = settings.SSLCOMMERZE_STORE_ID
SSLCOMMERZE_API_KEY = settings.SSLCOMMERZE_API_KEY


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
                    user = request.user
                    order = Order.objects.get(id=id, user=request.user)
                    payment = SSLCSession(
                        sslc_is_sandbox=True, sslc_store_id=SSLCOMMERZE_STORE_ID, sslc_store_pass=SSLCOMMERZE_API_KEY
                    )
                    status_url = request.build_absolute_uri(
                        reverse("payment-complete"))
                    payment.set_urls(
                        success_url=status_url,
                        fail_url=status_url,
                        cancel_url=status_url,
                        ipn_url=status_url
                    )
                    payment.set_product_integration(
                        total_amount=Decimal(order.amount),
                        currency='BDT',
                        product_category='Mixed',
                        product_name='order_items',
                        num_of_item=1,
                        shipping_method='Courier',
                        product_profile='None'
                    )
                    payment.set_customer_info(
                        name=user.full_name,
                        email=user.email,
                        address1=order.address,
                        city="Dhaka",
                        postcode="1100",
                        country="Bangladesh",
                        phone=order.phone
                    )
                    payment.set_shipping_info(
                        shipping_to=user.full_name,
                        address=order.address,
                        city="Dhaka",
                        postcode="1100",
                        country="Bangladesh",
                    )
                    payment.set_additional_values(
                        value_a=order.id
                    )
                    response = payment.init_payment()
                    order.pending_payment_url = response['GatewayPageURL']
                    order.save()
                    return Response(response, status=200)
                except Exception as e:
                    return Response({'msg': 'something went wrong', 'error': str(e)}, status=500)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class PaymentCompleteAPIView(APIView):
    def post(self, request, *args, **kwargs):
        payment_data = request.POST
        status = payment_data['status']
        order = Order.objects.get(id=payment_data['value_a'])
        if status == 'VALID':
            val_id = payment_data['val_id']
            order.txnid = payment_data['tran_id']
            order.is_paid = True
            order.status = 'paid'
            order.is_ordered = True
            order.save()
            success_url = settings.SITE_URL + 'order?success=true'
            return redirect(success_url)
        elif status == 'FAILED':
            order.status = 'stole'
            order.save()
            cancel_url = settings.SITE_URL + '?canceled=true'
            return redirect(cancel_url)


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
                query = Q() | Q(status="paid") | Q(status="on_the_way")
                order_list = Order.objects.filter(
                    query).order_by('-created_at')
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


class AssignDeliverManAPIView(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                order = self.get_object(pk)
                serializer = DeliverSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                order = self.get_object(pk)
                serializer = CreateDeliverSerializer(
                    order, data=request.data, partial=True)
                if serializer.is_valid():
                    if request.data.get('deliver_user'):
                        print('way')
                        serializer.save(status='on_the_way')
                    else:
                        print('paid')
                        serializer.save(status='paid')
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class OrderStatusAPIView(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                order = self.get_object(pk)
                serializer = OrderStatusSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.user.type == "seller":
                order = self.get_object(pk)
                serializer = OrderStatusSerializer(
                    order, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeliveryOrderAPIView(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            if request.user.type == "deliver":
                order_list = Order.objects.filter(
                    deliver_user=request.user).order_by('-created_at')
                serializer = DeliverOrderSerializer(order_list, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, format=None):
        if request.user.is_authenticated:
            if request.user.type == "deliver":
                order = Order.objects.get(id=request.data['id'])
                serializer = OrderStatusSerializer(
                    order, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class TotalIncomeAPIView(APIView):
    def get(self, request, *kwargs):
        order = Order.objects.aggregate(income=Sum('amount'))
        return Response(order, status=status.HTTP_200_OK)


class TotalIncomeByYearAPIView(APIView):
    def get(self, request, *kwargs):
        orders = Order.objects.all()
        lis = set([order.created_at.year for order in orders])
        final = list()
        for year in lis:
            dic = dict()
            orders = Order.objects.filter(
                created_at__year=year).aggregate(year_income=Sum('amount'))
            dic['year'] = year
            dic['income'] = orders['year_income']
            final.append(dic)
        return Response(final, status=status.HTTP_200_OK)


class TotalIncomeByMonthAPIView(APIView):
    def get(self, request, year, *kwargs):
        orders = Order.objects.filter(created_at__year=year)
        lis = set([order.created_at.month for order in orders])
        final = [
            {"name": "January", "value": 1, "amount": "-"},
            {"name": "February", "value": 2, "amount": "-"},
            {"name": "March", "value": 3, "amount": "-"},
            {"name": "April", "value": 4, "amount": "-"},
            {"name": "May", "value": 5, "amount": "-"},
            {"name": "June", "value": 6, "amount": "-"},
            {"name": "July", "value": 7, "amount": "-"},
            {"name": "August", "value": 8, "amount": "-"},
            {"name": "September", "value": 9, "amount": "-"},
            {"name": "October", "value": 10, "amount": "-"},
            {"name": "November", "value": 11, "amount": "-"},
            {"name": "December", "value": 12, "amount": "-"},
        ]
        for i in final:
            for month in lis:
                if i['value'] == month:
                    orders = Order.objects.filter(
                        created_at__month=month).aggregate(month_income=Sum('amount'))
                    i['amount'] = orders['month_income']
        return Response(final, status=status.HTTP_200_OK)


class TotalIncomeByDayAPIView(APIView):
    def get(self, request, year, month, *kwargs):
        q = Q() & Q(created_at__year=year) & Q(created_at__month=month)
        orders = Order.objects.filter(q)
        lis = set([order.created_at.day for order in orders])
        final = [
            {"day": 1, "amount": "-"},
            {"day": 2, "amount": "-"},
            {"day": 3, "amount": "-"},
            {"day": 4, "amount": "-"},
            {"day": 5, "amount": "-"},
            {"day": 6, "amount": "-"},
            {"day": 7, "amount": "-"},
            {"day": 8, "amount": "-"},
            {"day": 9, "amount": "-"},
            {"day": 10, "amount": "-"},
            {"day": 11, "amount": "-"},
            {"day": 12, "amount": "-"},
            {"day": 13, "amount": "-"},
            {"day": 14, "amount": "-"},
            {"day": 15, "amount": "-"},
            {"day": 16, "amount": "-"},
            {"day": 17, "amount": "-"},
            {"day": 18, "amount": "-"},
            {"day": 19, "amount": "-"},
            {"day": 20, "amount": "-"},
            {"day": 21, "amount": "-"},
            {"day": 22, "amount": "-"},
            {"day": 23, "amount": "-"},
            {"day": 24, "amount": "-"},
            {"day": 25, "amount": "-"},
            {"day": 26, "amount": "-"},
            {"day": 27, "amount": "-"},
            {"day": 28, "amount": "-"},
            {"day": 29, "amount": "-"},
            {"day": 30, "amount": "-"},
            {"day": 31, "amount": "-"},
        ]
        for i in final:
            for day in lis:
                if i['day'] == day:
                    orders = Order.objects.filter(
                        created_at__day=day).aggregate(day_income=Sum('amount'))
                    i['amount'] = orders['day_income']
        return Response(final, status=status.HTTP_200_OK)


class DayIncomeAPIView(APIView):
    def get(self, request, year, month, day, *kwargs):
        q = Q() & Q(created_at__year=year) & Q(
            created_at__month=month) & Q(created_at__day=day)
        orders = Order.objects.filter(q).aggregate(day_income=Sum('amount'))
        orders["day"] = int(day)
        return Response(orders, status=status.HTTP_200_OK)
