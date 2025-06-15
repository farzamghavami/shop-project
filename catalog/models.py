from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Time

User = get_user_model()
from accounts.models import Address, User


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return " / ".join(full_path[::-1])

    is_active = models.BooleanField(default=True)


class Shop(Time):
    STATUS_CHOICES = (
        ("PENDING", "pending"),
        ("APPROVED", "approved"),
        ("REJECTED", "rejected"),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shops")
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="PENDING")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="shops")
    is_active = models.BooleanField(default=True)


class Product(Time):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    is_active = models.BooleanField(default=True)
    image_url = models.CharField(max_length=200, null=True, blank=True)


class Wishlist(Time):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="wishlists"
    )
    is_active = models.BooleanField(default=True)

    # avoid repetition
    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} -> {self.product.name}"
