import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from accounts.models import User,Address,City,Country
from catalog.models import Shop, Category, Product
from orders.models import Order

# CREATING TEST MODELS FOR ALL AF THE MODELS IN FIXTURE

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
        password1="root",
        password2="root",
        phone="123153533",
        is_staff=True,
        is_superuser=True
    )

@pytest.fixture
def regular_user(django_user_model):
    return django_user_model.objects.create_user(
        username="user", email="user@test.com", password1="user123", password2="user123", phone="1231535"
    )

@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        email='another@example.com',
        username='anotheruser',
        password1='anotherpass123',
        password2='anotherpass123',
        is_staff=False,
        is_superuser=False
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