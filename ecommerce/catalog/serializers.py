from rest_framework import serializers
from accounts.serializers import UserSerializer,AddressSerializer
from accounts.models import Address, User
from accounts.serializers import UserSerializer
from .models import Product, Category, Shop, Wishlist


class CategorySerializer(serializers.ModelSerializer):
    # parent = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ["id", "name", "parent"]

    def to_representation(self, instance):
        rep= super().to_representation(instance)

        if instance.parent:
            rep["parent"] = {
                'id': instance.parent.id,
                'name': instance.parent.name
            }
        # if instance.user:
        #     rep["user"] = {
        #         'id': instance.user.id,
        #         'name': instance.user.username
        #
        #     }
        return rep


class ShopSerializer(serializers.ModelSerializer):
    owner=UserSerializer(read_only=True)
    address =serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())

    class Meta:
        model = Shop
        fields = ["id", "name", "owner", "address", "status", "is_active"]
        extra_kwargs = {"owner": {"read_only": True}}

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        if instance.address:
            rep["address"] = AddressSerializer(instance.address).data
        return rep


class ProductSerializer(serializers.ModelSerializer):
    shop = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category",
            "shop",
            "is_active",
            "image_url",
        ]
        extra_kwargs = {"is_active": {"read_only": True}}

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["shop"] = ShopSerializer(instance.shop).data
        rep["category"] = CategorySerializer(instance.category).data
        return rep




class WishListSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = Wishlist
        fields = [
            "id",
            "user",
            "product",
            "is_active",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"user": {"read_only": True},"created_at": {"read_only": True},"updated_at": {"read_only": True}}
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["user"] = UserSerializer(instance.user).data
        rep["product"] = ProductSerializer(instance.product).data
        return rep
