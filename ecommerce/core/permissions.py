from rest_framework.permissions import BasePermission
from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class IsSellerOrAdmin(BasePermission):
    """
    فقط کاربران SELLER یا ادمین‌ها اجازه ایجاد فروشگاه دارند.
    """

    def has_permission(self, request, view):
        return (
                request.user.is_authenticated and (
                request.user.role == 'SELLER' or
                request.user.is_staff or
                request.user.is_superuser
        )
        )


# class IsOwnerOrAdmin(permissions.BasePermission):
#     """
#     Object-level permission to only allow owners of an object to edit it.
#     Assumes the model instance has an `owner` attribute.
#     """
#
#     def has_object_permission(self, request, view, obj):
#         return obj.owner == request.user or request.user.is_staff

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only allow object owner to edit; anyone can read.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user



class IsOwnerOrAdmin(BasePermission):
    """
    اجازه فقط برای ادمین یا صاحب آبجکت.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True

        user = self._extract_user(obj)
        return user == request.user

    def _extract_user(self, obj):
        """
        استخراج کاربر از آبجکت یا آبجکت‌های مرتبط.
        """
        # اگر خود obj از جنس User باشه
        if isinstance(obj, User):
            return obj

        # حالت مستقیم
        for attr in ['user', 'owner']:
            if hasattr(obj, attr):
                return getattr(obj, attr)

        # حالت غیرمستقیم
        for relation in ['order', 'shop', 'product']:
            related_obj = getattr(obj, relation, None)
            if related_obj:
                for attr in ['user', 'owner']:
                    if hasattr(related_obj, attr):
                        return getattr(related_obj, attr)

        return None

