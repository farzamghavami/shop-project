import pytest


@pytest.mark.django_db
class TestUserModel():
    def test_user_model(self, user):
        user = user
        assert user.username == 'testuser'
        assert user.email == 'test@test.com'
        assert user.phone == '1231535'
        assert user.check_password('test1234/') is True




@pytest.mark.django_db
class TestAddressModel:
    def test_create_address_valid(self,address,user,city):

        address =address
        assert address.user == user
        assert address.city == city
        assert address.street == "test"
        assert address.zip_code == "123456"

@pytest.mark.django_db
class TestCityModel:
    def test_create_city_valid(self,city,country):
        city = city
        assert city.name == "test"
        assert city.country == country

@pytest.mark.django_db
class TestCountryModel:
    def test_create_country_valid(self,country):
        country = country
        assert country.name == "iran"

