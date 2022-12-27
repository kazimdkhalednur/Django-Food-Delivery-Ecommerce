from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User
from products.models import Food

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()

    def __str__(self):
        return f"{self.food.title}  {self.quantity}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    txnid = models.CharField(max_length=200, blank=True)
    is_ordered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if self.user.type != 'buyer':
            return
        super(Order, self).save(*args, **kwargs)

    def clean(self):
        if self.user.type != 'buyer':
            raise ValidationError({"user": "User type must be Buyer"})
