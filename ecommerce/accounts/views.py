from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .models import User, Address, Country, City
from .serializers import (
    UserSerializer,
    AddressSerializer,
    CountrySerializer,
    CitySerializer,
    ChangePasswordSerializer,
)
from django.shortcuts import get_object_or_404
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.permissions import IsOwnerOrAdmin
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView


@extend_schema(
    tags=["Users"],
    parameters=[
        OpenApiParameter(
            name="is_active",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="filter for active users",
        ),
        OpenApiParameter(
            name="is_staff",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="filter for staff users(true or false)",
        ),
        OpenApiParameter(
            name="search",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="search by username, email,date joined",
        ),
        OpenApiParameter(
            name="ordering",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="ordering by username, email and date joined)",
        ),
    ],
)

class UserList(ListAPIView):
    """
    user list
    """

    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active", "is_staff"]
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering_fields = ["username", "email", "date_joined"]


@extend_schema(tags=["Users"])
class UserDetail(APIView):
    """
    account detail
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = UserSerializer

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        srz_data = self.serializer_class(user)
        return Response(srz_data.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Users"])
class UserCreate(APIView):
    """
    create a new user
    """

    serializer_class = UserSerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Users"])
class UserUpdate(APIView):
    """
    update a user
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = UserSerializer

    def put(self, request, pk):
        queryset = get_object_or_404(User, id=pk)
        self.check_object_permissions(request, queryset)
        srz_data = self.serializer_class(queryset, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Users"])
class UserDelete(APIView):
    """
    user delete
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = UserSerializer

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.is_active = False
        user.save()
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Addresses"])
class AddressList(APIView):
    """
    address list
    """

    permission_classes = [IsAdminUser]
    serializer_class = AddressSerializer

    def get(self, request):
        queryset = Address.objects.all()
        self.check_object_permissions(request, queryset)
        srz_data = self.serializer_class(queryset, many=True)
        return Response(srz_data.data)


@extend_schema(tags=["Addresses"])
class AddressDetail(APIView):
    """address detail"""

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = AddressSerializer

    def get(self, request, pk):
        address = get_object_or_404(Address, pk=pk)
        self.check_object_permissions(request, address)
        srz_data = self.serializer_class(address)
        return Response(srz_data.data)


@extend_schema(tags=["Addresses"])
class AddressCreate(APIView):
    """
    create a new address
    """

    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def post(self, request):
        current_user = get_current_user_from_token(request)
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            srz_data.save(user=current_user)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        print(srz_data.errors)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Addresses"])
class AddressUpdate(APIView):
    """
    update a address
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = AddressSerializer

    def put(self, request, pk):
        queryset = get_object_or_404(Address, pk=pk)
        self.check_object_permissions(request, queryset)
        srz_data = self.serializer_class(queryset, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Addresses"])
class AddressDelete(APIView):
    """
    address delete
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = AddressSerializer

    def delete(self, request, pk):
        address = get_object_or_404(Address, id=pk)
        self.check_object_permissions(request, address)
        address.is_active = False
        address.save()
        serializer = self.serializer_class(address)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Countries"])
class CountryList(APIView):
    """
    country list
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CountrySerializer

    def get(self, request):
        queryset = Country.objects.all()
        srz_data = self.serializer_class(queryset, many=True)
        return Response(srz_data.data)


@extend_schema(tags=["Cities"])
class CityList(APIView):
    """
    city list
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CitySerializer

    def get(self, request):
        queryset = City.objects.all()
        srz_data = self.serializer_class(queryset, many=True)
        return Response(srz_data.data)


@extend_schema(tags=["ChangePassword"])
class ChangePasswordView(generics.GenericAPIView):
    """
    change password with valid password
    """

    permission_classes = [IsOwnerOrAdmin]
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "your password changed!!"}, status=200)
        return Response(serializer.errors, status=400)


"""for getting user ID in heather of token"""


def get_current_user_from_token(request):
    # استخراج توکن از header
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise AuthenticationFailed("توکن یافت نشد یا فرمت اشتباه است.")

    token = auth_header.split(" ")[1]

    try:
        # دیکود کردن توکن با secret key
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")

        if user_id is None:
            raise AuthenticationFailed("توکن معتبر نیست.")

        try:
            user = User.objects.get(id=user_id)
            return user

        except User.DoesNotExist:
            raise AuthenticationFailed("کاربر یافت نشد.")

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("توکن منقضی شده.")

    except jwt.InvalidTokenError:
        raise AuthenticationFailed("توکن نامعتبر است.")
