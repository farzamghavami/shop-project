from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Category, Product, Shop, Wishlist
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ShopSerializer,
    WishListSerializer,
)
from accounts.views import get_current_user_from_token
from core.permissions import *
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse


class ProductList(ListAPIView):

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    search_fields = ["description", "name"]

    ordering_fields = ["created_at", "updated_at"]

    filterset_fields = ["category", "is_active", "created_at", "updated_at"]


@extend_schema(tags=["products"])
class ProductDetail(APIView):
    """
    detail single product
    """

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        queryset = get_object_or_404(Product, pk=pk)
        srz_data = self.serializer_class(queryset)
        return Response(srz_data.data)


@extend_schema(tags=["products"])
class ProductCreate(APIView):
    """
    create new product
    """

    permission_classes = [IsSellerOrAdmin]
    serializer_class = ProductSerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["products"])
class ProductUpdate(APIView):
    """
    Update single product
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = ProductSerializer

    def put(self, request, pk):
        queryset = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(request, queryset)
        srz_data = self.serializer_class(queryset, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["products"])
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
        serializer = self.serializer_class(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["shops"])
class ShopList(ListAPIView):
    """
    List all shops
    """

    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]
    queryset = Shop.objects.all()


@extend_schema(tags=["shops"])
class ShopDetail(APIView):
    """
    detail single shop
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer

    def get(self, request, pk):
        shop = get_object_or_404(Shop, pk=pk)
        self.check_object_permissions(request, shop)
        srz_data = self.serializer_class(shop)
        return Response(srz_data.data)


@extend_schema(tags=["shops"])
class ShopCreate(APIView):
    """
    create shop
    """

    permission_classes = [IsSellerOrAdmin]
    serializer_class = ShopSerializer

    def post(self, request):
        #using token from user to create shop(you can know who create)
        current_user = get_current_user_from_token(request)
        self.check_object_permissions(request, request)
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            srz_data.save(owner=current_user)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["shops"])
class ShopUpdate(APIView):
    """
    update single shop
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = ShopSerializer

    def put(self, request, pk):
        queryset = get_object_or_404(Shop, pk=pk)
        self.check_object_permissions(request, queryset)
        srz_data = self.serializer_class(queryset, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["shops"])
class ShopDelete(APIView):
    """
    delete single shop
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = ShopSerializer

    def delete(self, request, pk):
        shop = get_object_or_404(Shop, pk=pk)
        self.check_object_permissions(request, shop)
        shop.is_active = False
        shop.save()
        serializer = self.serializer_class(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["categories"])
class CategoryList(APIView):
    """
    list all categories
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get(self, request):
        queryset = Category.objects.all()
        self.check_object_permissions(request, queryset)
        srz_data = CategorySerializer(queryset, many=True)
        return Response(srz_data.data)


@extend_schema(tags=["categories"])
class CategoryDetail(APIView):
    """
    detail single category
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        srz_data = self.serializer_class(category)
        return Response(srz_data.data)


@extend_schema(tags=["categories"])
class CategoryCreate(APIView):
    """
    create new category
    """

    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["categories"])
class CategoryUpdate(APIView):
    """
    update single category
    """

    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer

    def put(self, request, pk):
        queryset = get_object_or_404(Category, pk=pk)
        srz_data = self.serializer_class(queryset, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["categories"])
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
        serializer = self.serializer_class(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["wishlist"])
class WishlistList(APIView):
    """
    list all wishlist
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = WishListSerializer

    def get(self, request):
        queryset = Wishlist.objects.all()
        srz_data = self.serializer_class(queryset, many=True)
        return Response(srz_data.data)


@extend_schema(tags=["wishlist"])
class WishlistCreate(APIView):
    """
    Create new wishlist
    """

    permission_classes = [IsAuthenticated]
    serializer_class = WishListSerializer

    def post(self, request):
        current_user = get_current_user_from_token(request)
        queryset = self.serializer_class(data=request.data)
        self.check_object_permissions(request, queryset)

        if queryset.is_valid():
            product_id = queryset.validated_data.get("product").id

            # search for being exists
            if Wishlist.objects.filter(
                user=current_user, product_id=product_id
            ).exists():
                return Response(
                    {"detail": "this product is in the wishlist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # save if not saved before
            queryset.save(user=current_user)
            return Response(queryset.data, status=status.HTTP_201_CREATED)

        return Response(queryset.errors, status=status.HTTP_400_BAD_REQUEST)


class WishListDetail(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = WishListSerializer

    def get(self, request, pk):
        wishlist = get_object_or_404(Wishlist, pk=pk)
        srz_data = self.serializer_class(wishlist)
        return Response(srz_data.data)


@extend_schema(tags=["wishlist"])
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
        serializer = self.serializer_class(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)
