from decimal import Decimal
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Order


@receiver(post_save, sender=Order)
def update_order_amount(sender, instance,created, **kwargs):
    if created:
        amount = Decimal(0.00)
        for food in instance.food.all():
            amount += food.price
        instance.amount = amount
        instance.txnid = 'ghteyytj'
        print("ok")
        print(instance.amount)
