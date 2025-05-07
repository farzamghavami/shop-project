from importlib.metadata import requires

from django.db.models.fields.json import CaseInsensitiveMixin
from rest_framework import serializers
from .models import User, Address, Country, City


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = City
        fields = ['id', 'name', 'country']

        """ this code is for showing all of thing in CountrySerializer """
        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep['country'] = CountrySerializer(instance.country).data
            return rep


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AddressSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    class Meta:
        model = Address
        fields = ['id', 'city','user', 'street', 'zip_code','is_active']
        extra_kwargs = {'user': {'read_only': True}}

