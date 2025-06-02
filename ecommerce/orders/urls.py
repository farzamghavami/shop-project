from django.urls import path

from interactions.urls import app_name
from .views import (
    OrderList,
    OrderDetail,
    OrderCreate,
    OrderUpdate,
    OrderDelete,
    OrderItemList,
    OrderItemDetail,
    OrderItemUpdate,
    OrderItemDelete,
    DeliveryCreate,
    DeliveryDelete,
    DeliveryList,
    DeliveryDetail,
)

app_name = "orders"

urlpatterns = [
    path("order", OrderList.as_view(), name="order-list"),
    path("order/<int:pk>", OrderDetail.as_view(), name="order-detail"),
    path("order/create", OrderCreate.as_view(), name="order-create"),
    path("order/update/<int:pk>", OrderUpdate.as_view(), name="order-update"),
    path("order/delete/<int:pk>", OrderDelete.as_view(), name="order-delete"),
    path("orderitem", OrderItemList.as_view(), name="orderitem-list"),
    path("orderitem/<int:pk>", OrderItemDetail.as_view(), name="orderitem-detail"),
    path("orderitem/update/<int:pk>", OrderItemUpdate.as_view(), name="orderitem-update"),
    path("orderitem/delete/<int:pk>", OrderItemDelete.as_view(), name="orderitem-delete"),
    path("delivery", DeliveryList.as_view(), name="delivery-list"),
    path("delivery/<int:pk>", DeliveryDetail.as_view(), name="delivery-detail"),
    path("delivery/create", DeliveryCreate.as_view(), name="delivery-create"),
    path("delivery/delete/<int:pk>", DeliveryDelete.as_view(), name="delivery-delete"),
]
