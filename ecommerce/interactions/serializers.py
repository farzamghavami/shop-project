from rest_framework import serializers
from .models import Rate, Comment
from accounts.serializers import UserSerializer
from catalog.serializers import ProductSerializer


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['id', 'user', 'product', 'score']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'product', 'text', 'parent']