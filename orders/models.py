import uuid
from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User
from products.models import Food


class Cart(models.Model):
    RATING = {
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    review = models.CharField(max_length=500, blank=True, null=True)
    rating = models.CharField(
        max_length=5, choices=RATING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food.title}  {self.quantity}"

    def save(self, *args, **kwargs):
        if self.user.type != 'buyer':
            return
        super(Cart, self).save(*args, **kwargs)

    def clean(self):
        if self.user.type != 'buyer':
            raise ValidationError({"user": "User type must be Buyer"})


class Order(models.Model):
    ORDER_STATUS_CHOICES = {
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('on_the_way', 'On The Way'),
        ('delivered', 'Delivered'),
        ('stolen', 'Stolen'),
    }
    order_id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart, blank=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    txnid = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)
    pending_payment_url = models.CharField(
        max_length=1000, blank=True, null=True)
    is_ordered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if self.user.type != 'buyer':
            return
        if self.status != "pending":
            self.pending_payment_url = None
        super(Order, self).save(*args, **kwargs)

    def clean(self):
        if self.user.type != 'buyer':
            raise ValidationError({"user": "User type must be Buyer"})
