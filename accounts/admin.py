from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Address, City, Country


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "is_active", "is_superuser", "role")
    list_filter = ("email", "is_active", "is_superuser")
    search_fields = ("email",)
    ordering = ("-created_at",)
    fieldsets = (
        ("Authentications", {"fields": ("email", "password", "username")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active", "role")}),
        ("Group Permission", {"fields": ("groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "phone",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Address)
admin.site.register(City)
admin.site.register(Country)
