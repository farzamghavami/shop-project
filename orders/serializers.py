from rest_framework import serializers

from catalog.models import Product
from .models import Order, OrderItem, Delivery,Coupon


class ApplyCouponSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, value):
        try:
            coupon = Coupon.objects.get(code=value)
        except Coupon.DoesNotExist:
            raise serializers.ValidationError("کد تخفیف نامعتبر است")

        if not coupon.is_valid():
            raise serializers.ValidationError("کد تخفیف منقضی شده یا غیرفعال است")

        return value




class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["product", "count", "row_price", "order"]
        extra_kwargs = {"row_price": {"read_only": True}}


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["shop", "user", "address", "items", "total_price"]
        extra_kwargs = {"user": {"read_only": True}, "total_price": {"read_only": True}}

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        total_price = 0
        for item_data in items_data:
            product = item_data["product"]
            count = item_data["count"]
            row_price = product.price * count
            OrderItem.objects.create(
                order=order, product=product, count=count, row_price=row_price
            )
            total_price += row_price

        order.total_price = total_price
        order.save()
        return order


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ["id", "order", "method"]
