from django.db.models.fields.json import CaseInsensitiveMixin
from jsonschema import ValidationError
from rest_framework import serializers
from .models import User, Address, Country, City
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = City
        fields = ["id", "name", "country"]

        """ this code is for showing all of thing in CountrySerializer """

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep["country"] = CountrySerializer(instance.country).data
            return rep


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:

        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "role",
            "password",
            "password1",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "role": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError("Passwords must match")

        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return attrs

    """for hashing password"""

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    # """to responce just id and username"""
    # def to_representation(self, instance):
    #     # فقط id و username در پاسخ برگشت داده میشه
    #     return {
    #         'id': instance.id,
    #         'username': instance.username
    #     }


class AddressSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Address
        fields = [
            "id",
            "city",
            "user",
            "street",
            "zip_code",
            "is_active",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"user": {"read_only": True}}


class ChangePasswordSerializer(serializers.Serializer):
    """changing password from user"""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password1"]:
            raise serializers.ValidationError("password dosent match")

        validate_password(attrs["new_password"])

        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError("رمز فعلی اشتباه است.")

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
