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

class IsOwnerOrAdmin(BasePermission):
    """
    اجازه فقط برای ادمین یا صاحب آبجکت.
    سعی می‌کنه از آبجکت user رو استخراج کنه، چه مستقیم چه غیرمستقیم.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True

        user = self._extract_user(obj)

        return user == request.user

    def _extract_user(self, obj):
        """
        سعی می‌کنه فیلد user یا owner یا هرچیزی که به نوعی به user اشاره می‌کنه رو از آبجکت یا آبجکت‌های مرتبط پیدا کنه.
        """
        # حالت مستقیم: obj.user یا obj.owner
        for attr in ['user', 'owner']:
            if hasattr(obj, attr):
                return getattr(obj, attr)

        # حالت غیرمستقیم: مثل obj.order.user یا obj.shop.owner
        for relation in ['order', 'shop', 'product']:
            related_obj = getattr(obj, relation, None)
            if related_obj:
                for attr in ['user', 'owner']:
                    if hasattr(related_obj, attr):
                        return getattr(related_obj, attr)

        # هیچ چیز پیدا نکرد
        return None
