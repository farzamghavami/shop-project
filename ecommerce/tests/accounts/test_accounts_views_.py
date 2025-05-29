from http.client import responses
import pytest
from django.urls import reverse
from rest_framework import status
from tests.conftest import token_admin_client, regular_user, address

"""
TEST USER LIST
"""
@pytest.mark.django_db
class TestUserListView:
    @pytest.fixture
    def user_list_url(self):
        return reverse("accounts:users")

    def test_admin_can_view_user_list(self, user_list_url,token_admin_client,admin_user):
        response = token_admin_client.get(user_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert any(user["username"] == admin_user.username for user in response.json()["results"])

    def test_another_user_can_view_user_list(self, user_list_url,token_another_user_client,another_user):
        response = token_another_user_client.get(user_list_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


"""
TEST USER DETAIL
"""
@pytest.mark.django_db
class TestUserDetailView:
    @pytest.fixture
    def url(self,regular_user):
        return reverse("accounts:userdetail",kwargs={"pk": regular_user.pk})

    def test_admin_can_view_user_detail(self, token_admin_client, admin_user, regular_user,url):
        response = token_admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == regular_user.username


    def test_user_can_view_own_detail(self, regular_user, token_regular_user_client,url):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == regular_user.email

    def test_user_cannot_view_other_user_detail(self, url, token_another_user_client):
        response = token_another_user_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


"""
TEST USER UPDATE
"""

@pytest.mark.django_db
class TestUserUpdateView:
    @pytest.fixture
    def url(self,regular_user):
        return reverse("accounts:userupdate",kwargs={"pk": regular_user.pk})

    def test_admin_can_update_user_detail(self, token_admin_client, admin_user, regular_user, url):
        data = {"username": "admin_edited"}
        response = token_admin_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == "admin_edited"

    def test_user_can_update_own_info(self, url, regular_user, token_regular_user_client):
        data = {"username": "UpdatedName"}
        response = token_regular_user_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == "UpdatedName"

    def test_another_user_can_update_user_detail(self, url, token_another_user_client, another_user):
        data = {"username": "UpdatedName"}
        response = token_another_user_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

"""
TEST USER DELETE
"""

@pytest.mark.django_db
class TestUserDeleteView:
    @pytest.fixture
    def url(self,regular_user):
        return reverse("accounts:userdelete",kwargs={"pk": regular_user.pk})

    def test_admin_can_deactive_user(self, token_admin_client, admin_user, regular_user,url):
        response = token_admin_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        regular_user.refresh_from_db()
        assert regular_user.is_active is False

    def test_user_can_deactive_by_owner(self,url,token_regular_user_client,regular_user):
        response = token_regular_user_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        regular_user.refresh_from_db()
        assert regular_user.is_active is False

    def test_another_user_can_deactive_user(self,url,token_another_user_client,another_user):
        response = token_another_user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN



"""
TEST FOR ADDRESS LIST
"""

@pytest.mark.django_db
class TestAddressListView:
    @pytest.fixture
    def address_url(self,admin_user):
        return reverse("accounts:address-list")

    def test_admin_can_view_address_list(self, token_admin_client, admin_user, address_url):
        response = token_admin_client.get(address_url)
        assert response.status_code == status.HTTP_200_OK

    def test_user_can_view_address_list(self, address_url, token_regular_user_client,regular_user):
        response = token_regular_user_client.get(address_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN



"""
TEST FOR ADDRESS DETAIL
"""
@pytest.mark.django_db
class TestAddressDetailView:
    @pytest.fixture
    def address_detail_url(self,regular_user,address_regular_user):
        return reverse("accounts:address-detail",kwargs={"pk": address_regular_user.pk})

    def test_admin_can_view_address_detail(self, token_admin_client, admin_user, address_detail_url):
        response = token_admin_client.get(address_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_user_can_view_address_detail(self, address_detail_url, token_regular_user_client,regular_user):
        response = token_regular_user_client.get(address_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_another_user_view_address_detail(self, address_detail_url, token_another_user_client,another_user):
        response = token_another_user_client.get(address_detail_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        print(response.data)

"""
TEST FOR ADDRESS UPDATE
"""
@pytest.mark.django_db
class TestAddressUpdateView:
    @pytest.fixture
    def address_update_url(self,regular_user,address_regular_user):
        return reverse("accounts:address-update",kwargs={"pk": address_regular_user.pk})

    def test_admin_can_update_address(self, token_admin_client, admin_user, address_update_url):
        response = token_admin_client.put(address_update_url)
        assert response.status_code == status.HTTP_200_OK

    def test_user_can_update_address(self, address_update_url, token_regular_user_client,regular_user):
        response = token_regular_user_client.put(address_update_url)
        assert response.status_code == status.HTTP_200_OK

    def test_another_user_update_address(self, address_update_url, token_another_user_client,another_user):
        response = token_another_user_client.put(address_update_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

"""
TEST CHANGE PASSWORD
"""
@pytest.mark.django_db
class TestChangePasswordView:

    @pytest.fixture
    def url(self,regular_user):
        return reverse("accounts:change-password")

    def test_user_can_change_own_password_correct_old_password(self, token_regular_user_client, regular_user, url):
        data = {
            "old_password": "userpass123",  # رمز فعلی درست
            "new_password": "newstrongpass123",
            "new_password1": "newstrongpass123",
        }
        response = token_regular_user_client.put(url, data)
        print("Response status:", response.status_code)
        print("Response data:", response.json())
        assert response.status_code == status.HTTP_200_OK

    def test_user_can_change_own_password_incorrect_old_password(self, token_regular_user_client, regular_user, url):
        data = {
            "old_password": "<PASSWORD>", "new_password": "<PASSWORD>",
            "new_password1": "<PASSWORD213>",
            "new_password2": "<PASSWORD>213",
        }
        response = token_regular_user_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

