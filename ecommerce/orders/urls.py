from django.urls import path
from .views import Orderlist, Orderdetail, Ordercreate, Orderupdate, OrderDelete, OrderItemlist, OrderItemdetail, \
    OrderItemupdate, OrderItemDelete, OrderItemCreate, DeliveryCreate, DeliveryDelete, DeliveryList,DeliveryDetail

urlpatterns = [
    path('order', Orderlist.as_view()),
    path('order/<int:pk>', Orderdetail.as_view()),
    path('order/create', Ordercreate.as_view()),
    path('order/update/<int:pk>', Orderupdate.as_view()),
    path('order/delete/<int:pk>', OrderDelete.as_view()),
    path('orderitem', OrderItemlist.as_view()),
    path('orderitem/<int:pk>', OrderItemdetail.as_view()),
    path('orderitem/create', OrderItemCreate.as_view()),
    path('orderitem/update/<int:pk>', OrderItemupdate.as_view()),
    path('orderitem/delete/<int:pk>', OrderItemDelete.as_view()),
    path('delivery', DeliveryList.as_view()),
    path('delivery/<int:pk>', DeliveryDetail.as_view()),
    path('delivery/create', DeliveryCreate.as_view()),
    path('delivery/delete/<int:pk>', DeliveryDelete.as_view()),
]
