from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet

router = DefaultRouter()
router.register(r'', InvoiceViewSet, basename='invoice') # Changed r'invoices' to r''

urlpatterns = [
    path('', include(router.urls)),
]
