from django.urls import path
from .views import (
    ProductList,
    ProductDetail,
    ProductCreate,
    ProductUpdate,
    ProductDelete,
    ShopList,
    ShopDelete,
    ShopCreate,
    ShopUpdate,
    ShopDetail,
    CategoryList,
    CategoryDetail,
    CategoryCreate,
    CategoryUpdate,
    CategoryDelete,
    WishlistList,
    WishlistCreate,
    WishlistDelete,
    WishListDetail,
)

app_name = "catalog"

urlpatterns = [

    #this url is for product
    path("product", ProductList.as_view(), name="product-list"),
    path("product/<int:pk>", ProductDetail.as_view(), name="product-detail"),
    path("product/create", ProductCreate.as_view(), name="product-create"),
    path("product/update/<int:pk>", ProductUpdate.as_view(), name="product-update"),
    path("product/delete/<int:pk>", ProductDelete.as_view(), name="product-delete"),

    #this urls is for shop
    path("shop", ShopList.as_view(), name="shop-list"),
    path("shop/<int:pk>", ShopDetail.as_view(), name="shop-detail"),
    path("shop/create", ShopCreate.as_view(), name="shop-create"),
    path("shop/update/<int:pk>", ShopUpdate.as_view(), name="shop-update"),
    path("shop/delete/<int:pk>", ShopDelete.as_view(), name="shop-delete"),

    #this url is for category
    path("category", CategoryList.as_view(), name="category-list"),
    path("category/<int:pk>", CategoryDetail.as_view(), name="category-detail"),
    path("category/create", CategoryCreate.as_view(), name="category-create"),
    path("category/update/<int:pk>", CategoryUpdate.as_view(), name="category-update"),
    path("category/delete/<int:pk>", CategoryDelete.as_view(), name="category-delete"),

    #this url is for wishlist
    path("wishlist", WishlistList.as_view(), name="wishlist-list"),
    path("wishlist/<int:pk>", WishListDetail.as_view(), name="wishlist-detail"),
    path("wishlist/create", WishlistCreate.as_view(), name="wishlist-create"),
    path("wishlist/delete/<int:pk>", WishlistDelete.as_view(), name="wishlist-delete"),
]
