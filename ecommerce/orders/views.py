from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounts.views import get_current_user_from_token
from .models import Order, OrderItem, Delivery
from .serializers import (
    OrderSerializer,
    OrderItem,
    DeliverySerializer,
    OrderItemSerializer,
)
from core.permissions import IsOwnerOrAdmin, IsSellerOrAdmin
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["order"])
class OrderList(APIView):
    """
    list all orders
    """

    permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer

    def get(self, request):
        orders = Order.objects.all()
        self.check_object_permissions(request, orders)
        serializers = self.serializer_class(orders, many=True)
        return Response(serializers.data)


@extend_schema(tags=["order"])
class OrderDetail(APIView):
    """
    detail one order
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = OrderSerializer

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(request, order)
        serializer = self.serializer_class(order)
        return Response(serializer.data)


@extend_schema(tags=["order"])
class OrderCreate(APIView):
    """
    create a new order
    """

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request):
        currentUser = get_current_user_from_token(request)
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            serializers.save(user=currentUser)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["order"])
class OrderUpdate(APIView):
    """
    update an order
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = OrderSerializer

    def put(self, request, pk):
        queryset = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(request, queryset)
        serializers = self.serializer_class(queryset, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["order"])
class OrderDelete(APIView):
    """
    delete an order
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = OrderSerializer

    def delete(self, request, pk):
        object = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(request, object)
        object.is_active = False
        object.save()
        srz_data = self.serializer_class(object)
        return Response(srz_data.data, status=status.HTTP_204_NO_CONTENT)

@extend_schema(tags=["orderitem"])
class OrderItemList(APIView):
    """
    list all order items
    """

    permission_classes = [IsAdminUser]
    serializer_class = OrderItemSerializer

    def get(self, request):
        queryset = OrderItem.objects.all()
        for obj in queryset:
            self.check_object_permissions(request, obj)
        srz_data = self.serializer_class(queryset, many=True)
        return Response(srz_data.data)

@extend_schema(tags=["orderitem"])
class OrderItemDetail(APIView):
    """
    detail one order item
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = OrderItemSerializer

    def get(self, request, pk):
        orderitem = get_object_or_404(OrderItem, pk=pk)
        self.check_object_permissions(request, orderitem)
        serializers = self.serializer_class(orderitem)
        return Response(serializers.data)

@extend_schema(tags=["orderitem"])
class OrderItemUpdate(APIView):
    """
    update an order item
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = OrderItemSerializer

    def put(self, request, pk):
        queryset = get_object_or_404(OrderItem, pk=pk)
        self.check_object_permissions(request, queryset)
        srz_data = self.serializer_class(queryset, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["orderitem"])
class OrderItemDelete(APIView):
    """
    delete an order item
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = OrderItemSerializer

    def delete(self, request, pk):
        object = get_object_or_404(OrderItem, pk=pk)
        self.check_object_permissions(request, object)
        object.is_active = False
        object.save()
        srz_data = self.serializer_class(object)
        return Response(srz_data.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Delivery"])
class DeliveryList(APIView):
    """
    list all deliveries
    """

    permission_classes = [IsAuthenticated]
    serializer_class = DeliverySerializer

    def get(self, request):
        queryset = Delivery.objects.all()
        srz_data = self.serializer_class(queryset, many=True)
        return Response(srz_data.data)

@extend_schema(tags=["Delivery"])
class DeliveryDetail(APIView):
    """
    detail one delivery
    """

    permission_classes = [IsAuthenticated]
    serializer_class = DeliverySerializer

    def get(self, request, pk):
        queryset = get_object_or_404(Delivery, pk=pk)
        srz_data = self.serializer_class(queryset)
        return Response(srz_data.data)

@extend_schema(tags=["Delivery"])
class DeliveryCreate(APIView):
    """
    create a new delivery
    """

    permission_classes = [IsAdminUser]
    serializer_class = DeliverySerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Delivery"])
class DeliveryDelete(APIView):
    """
    delete an delivery
    """

    permission_classes = [IsAdminUser]
    serializer_class = DeliverySerializer

    def delete(self, request, pk):
        object = get_object_or_404(Delivery, pk=pk)
        object.is_active = False
        object.save()
        srz_data = self.serializer_class(object)
        return Response(srz_data.data, status=status.HTTP_200_OK)
