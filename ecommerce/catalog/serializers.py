from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Product, Category, Shop, Wishlist


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name','parent']


class ShopSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    class Meta:
        model = Shop
        fields = ['id', 'name', 'owner','address','status','is_active']
        extra_kwargs = {"owner": {"read_only": True}}

    """this method is for showing items that you want in UserSerializer """
    def get_owner(self, obj):
        return {
            "id": obj.owner.id,
            "name": obj.owner.username,}


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'shop','is_active','image_url']


class WishListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product',]