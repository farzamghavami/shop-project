import pytest
from _pytest.nodes import Item
from drf_yasg.openapi import Items
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from accounts.models import User, Address, City, Country
from catalog.models import Shop, Category, Product
from orders.models import Order, OrderItem, Delivery
from interactions.models import Comment

# CREATING TEST MODELS FOR ALL AF THE MODELS IN FIXTURE


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        email="test@test.com",
        password="test1234/",
        phone="1231535",
    )


@pytest.fixture
def country(db):
    return Country.objects.create(name="iran")


@pytest.fixture
def city(db, country):
    return City.objects.create(
        name="test",
        country=country,
    )


@pytest.fixture
def address(db, regular_user, city):
    return Address.objects.create(
        user=regular_user,
        city=city,
        street="test",
        zip_code="123456",
    )


@pytest.fixture
def shop(db, regular_user, address):

    return Shop.objects.create(
        status="PENDING",
        owner=regular_user,
        name="test",
        address=address,
        is_active=True,
    )


@pytest.fixture
def category(db):
    return Category.objects.create(name="lavazem electronici")


@pytest.fixture
def product(db, shop, category):
    return Product.objects.create(
        shop=shop,
        category=category,
        name="test",
        description="test",
        price=100,
        is_active=True,
    )


@pytest.fixture
def order(db, shop, user, address, regular_user):
    return Order.objects.create(
        shop=shop,
        user=regular_user,
        address=address,
        total_price=100,
    )


@pytest.fixture
def delivery(order):
    return Delivery.objects.create(order=order, method="TPOX")


@pytest.fixture
def comment(product, regular_user):
    return Comment.objects.create(
        product=product,
        text="this is a comment test",
        user=regular_user,
    )


@pytest.fixture
def api_client():
    client = APIClient()
    return client


# CREATING TEST USERS [ADMIN USER, REGULAR USER , ANOTHER USER]


@pytest.fixture
def admin_user(django_user_model):
    return django_user_model.objects.create_user(
        username="root",
        email="rooot@gmail.com",
        password="root1234/",
        phone="123153533",
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def regular_user(django_user_model):
    return django_user_model.objects.create_user(
        username="user",
        email="user@test.com",
        password="userpass123",  # ← اصلاح این خط
        phone="1231535444",
    )


@pytest.fixture
def another_user(django_user_model):
    return User.objects.create_user(
        email="another@example.com",
        username="anotheruser",
        password="anotherpass123",
        phone="123153544124",
        is_staff=False,
        is_superuser=False,
    )


@pytest.fixture
def seller_user():
    return User.objects.create_user(
        username="selleruser",
        email="seller@test.com",
        password="sellerpass123",
        phone="09121234567",
        role="SELLER",  # فرض بر اینکه فیلد نقش (role) دارید
    )


@pytest.fixture
def seller2_user():
    return User.objects.create_user(
        username="user2",
        email="user2@test.com",
        password="userpass123",
        phone="12315351251",
        role="SELLER",
    )


@pytest.fixture
def owner_user():
    return User.objects.create_user(
        email="another@example.com",
        username="anotheruser",
        password="anotherpass123",
        phone="12535441214",
        is_staff=False,
        is_superuser=False,
    )


# CREATING TEST TOKENS [ADMIN TOKEN, REGULAR USER TOKEN, ANOTHER USER TOKEN]


@pytest.fixture
def token_admin_client(admin_user):
    client = APIClient()
    token = AccessToken.for_user(admin_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def token_regular_user_client(regular_user):
    client = APIClient()
    token = AccessToken.for_user(regular_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def token_another_user_client(another_user):
    client = APIClient()
    token = AccessToken.for_user(another_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def token_seller_user_client(seller_user):
    client = APIClient()
    token = AccessToken.for_user(seller_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def token_seller2_user_client(seller2_user):
    client = APIClient()
    token = AccessToken.for_user(seller2_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def address_regular_user(db, regular_user, city):
    return Address.objects.create(
        user=regular_user,
        city=city,
        street="test",
        zip_code="123456",
    )


@pytest.fixture
def shop_seller_user(db, seller_user, address):
    return Shop.objects.create(
        status="PENDING",
        owner=seller_user,
        name="test",
        address=address,
        is_active=True,
    )


@pytest.fixture
def product_seller_user(seller_user, shop_seller_user, category):
    return Product.objects.create(
        shop=shop_seller_user,
        category=category,
        name="test",
        description="test",
        price=100,
        is_active=True,
    )


@pytest.fixture
def items(product):
    return OrderItem.objects.create(product=product, count=2)


@pytest.fixture
def create_order(shop, address, items):
    return Order.objects.create(
        shop=shop.id,
        address=address.id,
        items=items.id,
    )


@pytest.fixture
def order_item(order, product):
    return OrderItem.objects.create(
        order=order, product=product, count=2, row_price=product.price * 2
    )
