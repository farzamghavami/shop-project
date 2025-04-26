from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Category, Product, Shop, Wishlist
from .serializers import CategorySerializer, ProductSerializer, ShopSerializer, WishListSerializer
from accounts.views import get_current_user_from_token
from core.permissions import *


class ProductList(APIView):
    """
    list all products
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = Product.objects.all()
        srz_data = ProductSerializer(queryset, many=True)
        return Response(srz_data.data)


class ProductDetail(APIView):
    """
    detail single product
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        queryset = Product.objects.get(pk=pk)
        srz_data = ProductSerializer(queryset)
        return Response(srz_data.data)

class ProductCreate(APIView):
    """
    create new product
    """
    permission_classes = [IsSellerOrAdmin]
    serializer_class = ProductSerializer
    def post(self, request):
        srz_data = ProductSerializer(data=request.data)
        current_user = get_current_user_from_token(request)
        print(srz_data)
        if srz_data.is_valid():
            srz_data.save(user=current_user)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductUpdate(APIView):
    """
    update single product
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = ProductSerializer
    def put(self, request, pk):
        queryset = Product.objects.get(pk=pk)
        self.check_object_permissions(request, queryset)
        current_user = get_current_user_from_token(request)
        srz_data = ProductSerializer(queryset, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save(owner=current_user)
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDelete(APIView):
    """
    delete single product
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = ProductSerializer
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(request, product)
        product.is_active = False
        product.save()
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopList(APIView):
    """
    list all shops
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer
    def get(self, request):
        queryset = Shop.objects.all()
        srz_data = ShopSerializer(queryset, many=True)
        return Response(srz_data.data)


class ShopDetail(APIView):
    """
    detail single shop
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer
    def get(self, request, pk):
        shop = get_object_or_404(Shop, pk=pk)
        self.check_object_permissions(request, shop)
        srz_data = ShopSerializer(shop)
        return Response(srz_data.data)


class ShopCreate(APIView):
    """
    create new shop
    """
    permission_classes = [IsSellerOrAdmin]
    serializer_class = ShopSerializer
    def post(self, request):
        current_user = get_current_user_from_token(request)
        self.check_object_permissions(request, request)
        srz_data = ShopSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save(owner=current_user)  # 👈 اینجا owner رو ست می‌کنی
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopUpdate(APIView):
    """
    update single shop
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = ShopSerializer
    def put(self, request, pk):
        current_user = get_current_user_from_token(request)
        queryset = get_object_or_404(Shop, pk=pk)
        self.check_object_permissions(request, queryset)
        srz_data = ShopSerializer(queryset, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save(owner=current_user)
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopDelete(APIView):
    """
    delete single shop
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = ShopSerializer
    def delete(self, request, pk):
        current_user = get_current_user_from_token(request)
        shop = get_object_or_404(Shop, pk=pk)
        shop.is_active = False
        shop.save()
        serializer = ShopSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryList(APIView):
    """
    list all categories
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    def get(self, request):
        queryset = Category.objects.all()
        self.check_object_permissions(request,queryset)
        srz_data = CategorySerializer(queryset, many=True)
        return Response(srz_data.data)


class CategoryDetail(APIView):
    """
    detail single category
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        srz_data = CategorySerializer(category)
        return Response(srz_data.data)


class CategoryCreate(APIView):
    """
    create new category
    """
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer
    def post(self, request):
        current_user = get_current_user_from_token(request)
        srz_data = CategorySerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save(user=current_user)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryUpdate(APIView):
    """
    update single category
    """
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer
    def put(self, request, pk):
        queryset = get_object_or_404(Category, pk=pk)
        srz_data = CategorySerializer(queryset, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDelete(APIView):
    """
    delete single category
    """
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer
    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.is_active = False
        category.save()
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WishlistList(APIView):
    """
    list all wishlist
    """
    permission_classes = [IsAuthenticated]
    serializer_class = WishListSerializer
    def get(self, request):
        queryset = Wishlist.objects.all()
        srz_data = WishListSerializer(queryset, many=True)
        return Response(srz_data.data)


class WishlistCreate(APIView):
    """
    create new wishlist
    """
    permission_classes = [IsAuthenticated]
    serializer_class = WishListSerializer
    def post(self, request):
        current_user = get_current_user_from_token(request)
        queryset = WishListSerializer(data=request.data)
        self.check_object_permissions(request, queryset)
        if queryset.is_valid():
            queryset.save(user=current_user)
            return Response(queryset.data, status=status.HTTP_201_CREATED)
        return Response(queryset.errors, status=status.HTTP_400_BAD_REQUEST)


class WishlistDelete(APIView):
    """
    delete wishlist
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = WishListSerializer
    def delete(self, request, pk):
        wishlist = get_object_or_404(Wishlist, pk=pk)
        self.check_object_permissions(request, wishlist)
        wishlist.is_active = False
        wishlist.save()
        serializer = WishListSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)