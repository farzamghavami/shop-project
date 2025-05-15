from django.db import models
from django.db.models.fields import FloatField
from accounts.models import User, Address
from catalog.models import Product, Shop


class Order(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    row_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.count} x {self.product.name}"


class Delivery(models.Model):
    METHOD_CHOICES = (
        ("TPOX", "tpox"),
        ("POST", "post"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)

    def __str__(self):
        return f"Delivery for Order #{self.order.id} - {self.method}"
