from django.urls import  path
from .views import UserList, UserCreate, UserDelete, UserUpdate, AddressDetail, AddressCreate, AddressUpdate, \
    AddressDelete, UserDetail,AddressList,CityList,CountryList,ChangePasswordView

from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('users', UserList.as_view()),
    path('user/<int:pk>', UserDetail.as_view()),
    path('register', UserCreate.as_view()),
    path('change-password', ChangePasswordView.as_view()),
    path('user/delete/<int:pk>', UserDelete.as_view()),
    path('user/update/<int:pk>', UserUpdate.as_view()),
    path('address/<int:pk>',AddressDetail.as_view()),
    path('address',AddressList.as_view()),
    path('address/create', AddressCreate.as_view()),
    path('address/update/<int:pk>', AddressUpdate.as_view()),
    path('address/delete/<int:pk>', AddressDelete.as_view()),
    path('city', CityList.as_view()),
    path('country', CountryList.as_view()),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
]