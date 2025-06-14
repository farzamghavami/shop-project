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
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:

        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "role",
            "password1",
            "password2",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "role": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def validate(self, attrs):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise serializers.ValidationError("Passwords must match")

            try:
                validate_password(password1)
            except exceptions.ValidationError as e:
                raise serializers.ValidationError({"password1": list(e.messages)})

        return attrs

    """for hashing password"""

    def create(self, validated_data):
        password = validated_data.pop("password1")
        validated_data.pop("password2")

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    # """to responce just id and username"""
    # def to_representation(self, instance):
    #     # فقط id و username در پاسخ برگشت داده میشه
    #     return {
    #         'id': instance.id,
    #         'username': instance.username
    #     }


class AddressSerializer(serializers.ModelSerializer):
    # using serializers of user and city for mor information like name and id of city and user fild fore get method
    city = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

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

    """for getting more information about user and city(id,name)"""

    def get_city(self, obj):

        return {"id": obj.city.id, "name": obj.city.name}

    def get_user(self, obj):

        return {
            "id": obj.user.id,
            "name": obj.user.username,  # یا هر فیلدی که به عنوان نام کاربر دارید
        }


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
