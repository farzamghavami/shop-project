import pytest

from tests.conftest import regular_user


@pytest.mark.django_db
class TestUserModel:
    """test user model"""

    def test_user_model(self, user):
        user = user
        assert user.username == "testuser"
        assert user.email == "test@test.com"
        assert user.phone == "1231535"
        assert user.check_password("test1234/") is True


@pytest.mark.django_db
class TestAddressModel:
    """test address model"""

    def test_create_address_valid(self, address, regular_user, city):

        address = address
        assert address.user == regular_user
        assert address.city == city
        assert address.street == "test"
        assert address.zip_code == "123456"


@pytest.mark.django_db
class TestCityModel:
    """test city model"""

    def test_create_city_valid(self, city, country):
        city = city
        assert city.name == "test"
        assert city.country == country


@pytest.mark.django_db
class TestCountryModel:
    """test country model"""

    def test_create_country_valid(self, country):
        country = country
        assert country.name == "iran"
