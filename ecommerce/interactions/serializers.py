from rest_framework import serializers
from .models import Rate, Comment
from accounts.serializers import UserSerializer
from catalog.serializers import ProductSerializer


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['id', 'user', 'product', 'score']
        extra_kwargs = {'user': {'read_only': True}}
    score = serializers.IntegerField(min_value=0, max_value=5)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'product','user', 'text', 'parent']
        extra_kwargs = {'user': {'read_only': True}}


