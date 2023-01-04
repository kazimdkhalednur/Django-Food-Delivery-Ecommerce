from django.contrib import admin
from .models import Order, Cart, Review


# admin.site.register()
admin.site.register(Order)


@admin.register(Review)
class ReviewCustomizedAdmin(admin.ModelAdmin):
    list_display = ["id", "rating"]


@admin.register(Cart)
class CartCustomizedAdmin(admin.ModelAdmin):
    list_display = ["id"]
