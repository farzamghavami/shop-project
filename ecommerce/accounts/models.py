from django.db import models
from django.contrib.auth.models import AbstractUser


class Time(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, Time):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("SELLER", "Seller"),
        ("USER", "User"),
    )
    phone = models.CharField(max_length=36, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")
    is_active = models.BooleanField(default=True)
    password1 = models.CharField(max_length=128,)
    password2 = models.CharField(max_length=255,)

    def __str__(self):
        return f"{self.email} ({self.role})"


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities"
    )

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class Address(Time):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.city.name}"
