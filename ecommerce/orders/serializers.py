from rest_framework import serializers
from .models import Order, OrderItem, Delivery


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id','order', 'product', 'count', 'row_price']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'user', 'shop', 'address', 'total_price']


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'order','method']