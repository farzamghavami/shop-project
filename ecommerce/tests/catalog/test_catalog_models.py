import pytest
from django.db import IntegrityError
from catalog.models import *
User = get_user_model()


@pytest.mark.django_db
class TestCategoryModel:
    def test_create_category_no_parent(self):
        category = Category.objects.create(
            name = "lavazem electronici",
        )
        assert category.name == "lavazem electronici"
        assert category.parent is None

    def test_create_category_parent(self):
        parent = Category.objects.create(name = "lavazem electronici")
        child = Category.objects.create(name = "mobile", parent=parent)
        assert child.parent == parent
        assert child.name == "mobile"
        assert parent.name == "lavazem electronici"
        assert parent.children.first() == child

    def test_category_str_method(self):
        parent = Category.objects.create(name = "lavazem electronici")
        child = Category.objects.create(name = "mobile", parent=parent)
        sub_child = Category.objects.create(name = "iphone", parent=child)

        assert str(sub_child) == "lavazem electronici / mobile / iphone"

@pytest.mark.django_db
class TestShopModel:

    def test_create_shop(self,shop,user,address):
        shop = shop
        assert shop.owner == user
        assert shop.name == "test"
        assert shop.address == address
        assert shop.status == "PENDING"
        assert shop.is_active is True
        assert shop.created_at is not None

@pytest.mark.django_db
class TestProductModel:

    def test_create_product_no_parent(self,shop,category):
        product = Product.objects.create(
            shop = shop,
            category = category,
            name = "test",
            description = "test",
            price = 100,
            is_active = True,
        )
        assert product.shop == shop
        assert product.category == category
        assert product.name == "test"
        assert product.description == "test"
        assert product.price == 100
        assert product.is_active is True

@pytest.mark.django_db
class TestWishListModel:
    def test_create_wishlist(self,user,product):
        wishlist = Wishlist.objects.create(user = user, product = product)
        assert wishlist.user == user
        assert wishlist.product == product

    def test_wishlist_unique_together(self, user, product):
        Wishlist.objects.create(user=user, product=product)
        with pytest.raises(IntegrityError):
            Wishlist.objects.create(user=user, product=product)