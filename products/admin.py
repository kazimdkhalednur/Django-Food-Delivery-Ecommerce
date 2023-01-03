from django.contrib import admin
from .models import Food, Category, Review


admin.site.register(Category)
admin.site.register(Food)


@admin.register(Review)
class ReviewCustomizedAdmin(admin.ModelAdmin):
    list_display = ["rating", "food"]
