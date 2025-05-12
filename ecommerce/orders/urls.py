from django.urls import path
from .views import OrderList, OrderDetail, OrderCreate, OrderUpdate, OrderDelete, OrderItemList, OrderItemDetail, \
    OrderItemUpdate, OrderItemDelete, DeliveryCreate, DeliveryDelete, DeliveryList,DeliveryDetail

urlpatterns = [
    path('order', OrderList.as_view()),
    path('order/<int:pk>', OrderDetail.as_view()),
    path('order/create', OrderCreate.as_view()),
    path('order/update/<int:pk>', OrderUpdate.as_view()),
    path('order/delete/<int:pk>', OrderDelete.as_view()),
    path('orderitem', OrderItemList.as_view()),
    path('orderitem/<int:pk>', OrderItemDetail.as_view()),
    path('orderitem/update/<int:pk>', OrderItemUpdate.as_view()),
    path('orderitem/delete/<int:pk>', OrderItemDelete.as_view()),
    path('delivery', DeliveryList.as_view()),
    path('delivery/<int:pk>', DeliveryDetail.as_view()),
    path('delivery/create', DeliveryCreate.as_view()),
    path('delivery/delete/<int:pk>', DeliveryDelete.as_view()),
]
