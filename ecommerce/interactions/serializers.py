from rest_framework import serializers

from catalog.models import Product
from .models import Rate, Comment
from accounts.serializers import UserSerializer
from catalog.serializers import ProductSerializer



class RateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = Rate
        fields = ['id', 'user', 'product', 'score']
        read_only_fields = ['user']  # چون کاربر از توکن JWT استخراج میشه

    def validate_score(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("امتیاز باید بین ۱ تا ۵ باشد.")
        return value

    def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep["product"] = ProductSerializer(instance.product).data
            rep["user"] = UserSerializer(instance.user).data
            return rep

class CommentSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Comment
        fields = ["id", "product", "user", "text", "parent"]
        extra_kwargs = {"user": {"read_only": True}}

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["product"] = ProductSerializer(instance.product).data
        rep["parent"] = CommentSerializer(instance.parent).data
        return rep
