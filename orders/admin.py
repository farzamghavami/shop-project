
from django.contrib import admin
from .models import Coupon, Order


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percent", "valid_from", "valid_to", "active", "usage_count")
    list_filter = ("active",)
    search_fields = ("code",)

admin.site.register(Order)

