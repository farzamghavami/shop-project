from django.db import models
from accounts.models import User, Address, Time
from catalog.models import Product, Shop
from django.utils import timezone
from decimal import Decimal


# orders/models.py

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(help_text="persent of coupon")
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    max_usage = models.PositiveIntegerField(default=1)
    usage_count = models.PositiveIntegerField(default=0)
    min_order_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text="minimum order amount per coupon"
    )

    def is_valid(self,order_total: Decimal = None):
        now = timezone.now()
        if not self.active and self.valid_from <= now <= self.valid_to and self.usage_count <= self.max_usage:
            return False

        if order_total is not None and order_total < self.min_order_amount:
            return False

        return True


    def __str__(self):
        return self.code



class Order(Time):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    discount_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def calculate_total_price(self):
        # جمع کل محصولات
        items_total = sum([
            item.row_price * item.count for item in self.items.all()
        ])


        # محاسبه تخفیف به‌صورت Decimal امن
        if self.coupon and self.coupon.is_valid(order_total=items_total):
            discount_rate = Decimal(self.coupon.discount_percent) / Decimal('100')
            self.discount_amount = items_total * discount_rate
        else:
            self.discount_amount = Decimal('0')

        # قیمت نهایی با در نظر گرفتن تخفیف
        self.total_price = items_total - self.discount_amount

        return self.total_price



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



