from rest_framework import serializers
from .models import Product, Category, Shop, Wishlist


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name',]


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'owner','address','status','is_active']
        extra_kwargs = {"owner": {"read_only": True}}


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'shop','is_active','image_url']


class WishListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product',]