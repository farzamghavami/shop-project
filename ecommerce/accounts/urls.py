from django.urls import path
from .views import (
    UserList,
    UserCreate,
    UserDelete,
    UserUpdate,
    AddressDetail,
    AddressCreate,
    AddressUpdate,
    AddressDelete,
    UserDetail,
    AddressList,
    CityList,
    CountryList,
    ChangePasswordView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "accounts"
urlpatterns = [

    path("users", UserList.as_view(),name="users"),
    path("user/<int:pk>", UserDetail.as_view(),name="userdetail"),
    path("user/delete/<int:pk>", UserDelete.as_view(),name="userdelete"),
    path("user/update/<int:pk>", UserUpdate.as_view(),name="userupdate"),

    path("address/<int:pk>", AddressDetail.as_view(),name="address-detail"),
    path("address", AddressList.as_view(),name="address-list"),
    path("address/create", AddressCreate.as_view()),
    path("address/update/<int:pk>", AddressUpdate.as_view(),name="address-update"),
    path("address/delete/<int:pk>", AddressDelete.as_view()),

    #list of city and country
    path("city", CityList.as_view()),
    path("country", CountryList.as_view(),name="country-list"),
    #changing password
    path("change-password", ChangePasswordView.as_view(),name="change-password"),
    # register and login
    path("register", UserCreate.as_view(),name="register"),
    path("login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh-token", TokenRefreshView.as_view(), name="token_refresh"),
]
