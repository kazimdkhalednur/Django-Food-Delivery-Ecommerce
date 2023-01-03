from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User
from utils.misc import generate_slug, image_path, image_path_category


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to=image_path_category, blank=True)

    def __str__(self):
        return self.title


class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    image = models.ImageField(upload_to=image_path, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.user.type != 'seller':
            return
        if not self.slug:
            self.slug = generate_slug(self.title)
        super(Food, self).save(*args, **kwargs)

    def clean(self):
        if self.user.type != 'seller':
            raise ValidationError({"user": "User type must be Seller"})


class Review(models.Model):
    RATING = {
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    review = models.CharField(max_length=500)
    rating = models.CharField(max_length=5, choices=RATING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if self.user.type != 'buyer':
            return
        super(Review, self).save(*args, **kwargs)

    def clean(self):
        if self.user.type != 'buyer':
            raise ValidationError({"user": "User type must be Buyer"})
