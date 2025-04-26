from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from accounts.views import get_current_user_from_token
from .models import Order,OrderItem,Delivery
from .serializers import OrderSerializer, OrderItem, DeliverySerializer, OrderItemSerializer
from core.permissions import IsOwnerOrAdmin,IsSellerOrAdmin


class OrderList(APIView):
    """
    list all orders
    """
    permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer
    def get(self,request):
        queryset = Order.objects.all()
        serializers = OrderSerializer(queryset,many=True)
        return Response(serializers.data)

class OrderDetail(APIView):
    """
    detail one order
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = OrderSerializer
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(request,order)
        serializer = OrderSerializer(order)  # بدون many=True
        return Response(serializer.data)

class OrderCreate(APIView):
    """
    create a new order
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    def post(self,request):
        currentUser = get_current_user_from_token(request)
        serializers = OrderSerializer(data=request.data)
        self.check_object_permissions(request,serializers)
        if serializers.is_valid():
            serializers.save(user=currentUser)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderUpdate(APIView):
    """
    update an order
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = OrderSerializer
    def put(self,request,pk):
        queryset = Order.objects.get(pk=pk)
        self.check_object_permissions(request,queryset)
        serializers = OrderSerializer(queryset, data=request.data,partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDelete(APIView):
    """
    delete an order
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = OrderSerializer
    def delete(self,request,pk):
        object= get_object_or_404(Order, pk=pk)
        self.check_object_permissions(request,object)
        object.is_active = False
        object.save()
        srz_data = OrderSerializer(object)
        return Response(srz_data.data, status=status.HTTP_204_NO_CONTENT)

class OrderItemList(APIView):
    """
    list all order items
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = OrderItemSerializer
    def get(self,request):
        queryset = OrderItem.objects.all()
        # self.check_object_permissions(request,queryset)
        srz_data = OrderItemSerializer(queryset, many=True)
        return Response(srz_data.data)

class OrderItemDetail(APIView):
    """
    detail one order item
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = OrderItemSerializer
    def get(self,request,pk):
        orderitem = get_object_or_404(OrderItem, pk=pk)
        self.check_object_permissions(request,orderitem)
        serializers = OrderItemSerializer(orderitem)
        return Response(serializers.data)


class OrderItemupdate(APIView):
    """
    update an order item
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = OrderItemSerializer
    def put(self,request,pk):
        queryset = get_object_or_404(OrderItem, pk=pk)
        self.check_object_permissions(request,queryset)
        srz_data = OrderItemSerializer(queryset, data=request.data,partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderItemDelete(APIView):
    """
    delete an order item
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = OrderItemSerializer
    def delete(self,request,pk):
        object= get_object_or_404(OrderItem, pk=pk)
        self.check_object_permissions(request,object)
        object.is_active = False
        object.save()
        srz_data = OrderItemSerializer(object)
        return Response(srz_data.data, status=status.HTTP_200_OK)

class DeliveryList(APIView):
    """
    list all deliveries
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DeliverySerializer
    def get(self,request):
        queryset= Delivery.objects.all()
        srz_data = DeliverySerializer(queryset, many=True)
        return Response(srz_data.data)


class DeliveryDetail(APIView):
    """
    detail one delivery
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DeliverySerializer
    def get(self,request,pk):
        queryset = get_object_or_404(Delivery, pk=pk)
        srz_data = DeliverySerializer(queryset, many=True)
        return Response(srz_data.data)


class DeliveryCreate(APIView):
    """
    create a new delivery
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DeliverySerializer
    def post(self,request):
        srz_data = DeliverySerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryDelete(APIView):
    """
    delete an delivery
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DeliverySerializer
    def delete(self,request,pk):
        object= get_object_or_404(Delivery,pk=pk)
        object.is_active = False
        object.save()
        srz_data = DeliverySerializer(object)
        return Response(srz_data.data,status=status.HTTP_200_OK)







