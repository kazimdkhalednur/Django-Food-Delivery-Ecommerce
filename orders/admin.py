from django.contrib import admin
from .models import Order, Cart


admin.site.register(Cart)
admin.site.register(Order)
