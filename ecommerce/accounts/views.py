from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Address, Country,City
from .serializers import UserSerializer,AddressSerializer,CountrySerializer,CitySerializer
from django.shortcuts import get_object_or_404
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from core.permissions import IsOwnerOrAdmin,IsSellerOrAdmin
class UserList(APIView):
    """
    user list
    """
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    def get(self,request):
        queryset = User.objects.all()
        srz_data = UserSerializer(queryset, many=True)
        return Response(srz_data.data)

class UserDetail(APIView):
    """
    account detail
    """
    permission_classes = [IsAuthenticated,IsOwnerOrAdmin]
    serializer_class = UserSerializer
    def get(self,request,pk):
        queryset = User.objects.filter(id=pk)
        srz_data = UserSerializer(queryset, many=True)
        return Response(srz_data.data)



class UserCreate(APIView):
    """
    create a new user
    """
    serializer_class = UserSerializer
    def post(self,request):
        srz_data = UserSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdate(APIView):
    """
    update a user
    """
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = UserSerializer
    def put(self, request, pk):
        queryset = get_object_or_404(User, id=pk)
        self.check_object_permissions(request, queryset)
        srz_data = UserSerializer(queryset, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDelete(APIView):
    """
    user delete
    """
    permission_classes = [IsAuthenticated,IsOwnerOrAdmin]
    serializer_class = UserSerializer
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.is_active = False
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddressList(APIView):
    """
    address list
    """
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = AddressSerializer
    def get(self,request):
        queryset = Address.objects.all()
        self.check_object_permissions(request, queryset)
        srz_data = AddressSerializer(queryset, many=True)
        return Response(srz_data.data)

class AddressDetail(APIView):
    """address detail"""
    permission_classes = [IsAuthenticated,IsOwnerOrAdmin]
    serializer_class = AddressSerializer
    def get(self,request,pk):
        queryset = Address.objects.get(id=pk)
        self.check_object_permissions(request, queryset)
        srz_data = AddressSerializer(queryset)
        return Response(srz_data.data)

class AddressCreate(APIView):
    """
    create a new address
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    def post(self,request):
        srz_data = AddressSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        print(srz_data.errors)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class AddressUpdate(APIView):
    """
    update a address
    """
    permission_classes = [IsAuthenticated,IsOwnerOrAdmin]
    serializer_class = AddressSerializer
    def put(self,request,pk):
        queryset =Address.objects.get(id=pk)
        self.check_object_permissions(request, queryset)
        srz_data = AddressSerializer(queryset, data=request.data,partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class AddressDelete(APIView):
    """
    address delete
    """
    permission_classes = [IsAuthenticated,IsOwnerOrAdmin]
    serializer_class = AddressSerializer
    def delete(self,request,pk):
        address = get_object_or_404(Address, id=pk)
        self.check_object_permissions(request, address)
        address.is_active = False
        address.save()
        serializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CountryList(APIView):
    """
    country list
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CountrySerializer
    def get(self,request):
        queryset = Country.objects.all()
        srz_data = CountrySerializer(queryset, many=True)
        return Response(srz_data.data)

class CityList(APIView):
    """
    city list
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CitySerializer
    def get(self,request):
        queryset = City.objects.all()
        srz_data = CitySerializer(queryset, many=True)
        return Response(srz_data.data)




def get_current_user_from_token(request):
    # استخراج توکن از header
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        raise AuthenticationFailed('توکن یافت نشد یا فرمت اشتباه است.')

    token = auth_header.split(' ')[1]

    try:
        # دیکود کردن توکن با secret key
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get('user_id')

        if user_id is None:
            raise AuthenticationFailed('توکن معتبر نیست.')

        try:
            user = User.objects.get(id=user_id)
            return user

        except User.DoesNotExist:
            raise AuthenticationFailed('کاربر یافت نشد.')

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('توکن منقضی شده.')

    except jwt.InvalidTokenError:
        raise AuthenticationFailed('توکن نامعتبر است.')
