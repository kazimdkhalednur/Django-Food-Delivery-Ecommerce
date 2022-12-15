from django.contrib import admin
from .models import User


@admin.register(User)
class UserCustomizedAdmin(admin.ModelAdmin):
    list_display=["email"]