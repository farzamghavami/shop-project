import pytest
from accounts.models import User,Address,City,Country
from catalog.models import Shop, Category, Product
from orders.models import Order


@pytest.fixture
def user(db):
    return User.objects.create(
        username='testuser',
        email='test@test.com',
        password1='<PASSWORD>',
        password2='<PASSWORD>',
        phone='1231535',
    )

@pytest.fixture
def country(db):
    return Country.objects.create(name="iran")

@pytest.fixture
def city(db,country):
    return City.objects.create(
        name="test",
        country=country,
    )

@pytest.fixture
def address(db,user,city):
    return Address.objects.create(
        user=user,
        city=city,
        street="test",
        zip_code="123456",
    )

@pytest.fixture
def shop(db,user,address):

    return Shop.objects.create(
        status="PENDING",
        owner=user,
        name="test",
        address=address,
        is_active=True,
    )
@pytest.fixture
def category(db):
    return Category.objects.create(name="test")

@pytest.fixture
def product(db,shop,category):
    return Product.objects.create(
        shop=shop,
        category=category,
        name="test",
        description="test",
        price=100,
        is_active=True,
    )

@pytest.fixture
def order(db,shop,user,address):
    return Order.objects.create(
        shop=shop,
        user=user,
        address=address,
        total_price=100,
    )