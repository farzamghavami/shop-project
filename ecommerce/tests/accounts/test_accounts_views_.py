import pytest
from django.urls import reverse
from rest_framework import status
from tests.conftest import token_admin_client, regular_user, address


@pytest.mark.django_db
class TestUserListView:
    @pytest.fixture
    def user_list_url(self):
        return reverse("accounts:users")
    # admin can
    def test_admin_can_view_user_list(self, user_list_url,token_admin_client,admin_user):
        response = token_admin_client.get(user_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert any(user["username"] == admin_user.username for user in response.json()["results"])
    # other users cant
    def test_another_user_cannot_view_user_list(self, user_list_url,token_another_user_client,another_user):
        response = token_another_user_client.get(user_list_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN



@pytest.mark.django_db
class TestUserDetailView:
    """
    TEST USER DETAIL
    """
    @pytest.fixture
    def url(self,regular_user):
        return reverse("accounts:userdetail",kwargs={"pk": regular_user.pk})
    #admin can
    def test_admin_can_view_user_detail(self, token_admin_client, admin_user, regular_user,url):
        response = token_admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == regular_user.username
        print(response.json())

    # owner can
    def test_user_can_view_own_detail(self, regular_user, token_regular_user_client,url):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == regular_user.email
    #other users cant
    def test_user_cannot_view_other_user_detail(self, url, token_another_user_client):
        response = token_another_user_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN




@pytest.mark.django_db
class TestUserUpdateView:
    """
    TEST USER UPDATE
    """
    @pytest.fixture
    def url(self,regular_user):
        return reverse("accounts:userupdate",kwargs={"pk": regular_user.pk})
    #admin can
    def test_admin_can_update_user_detail(self, token_admin_client, admin_user, regular_user, url):
        data = {"username": "admin_edited"}
        response = token_admin_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == "admin_edited"
    #owner can
    def test_user_can_update_own_info(self, url, regular_user, token_regular_user_client):
        data = {"username": "UpdatedName"}
        response = token_regular_user_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == "UpdatedName"
    #other users cant
    def test_another_user_can_update_user_detail(self, url, token_another_user_client, another_user):
        data = {"username": "UpdatedName"}
        response = token_another_user_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN



@pytest.mark.django_db
class TestUserDeleteView:
    """
    TEST USER DELETE
    """
    @pytest.fixture
    def url(self,regular_user):
        return reverse("accounts:userdelete",kwargs={"pk": regular_user.pk})
    #admin can
    def test_admin_can_deactive_user(self, token_admin_client, admin_user, regular_user,url):
        response = token_admin_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        regular_user.refresh_from_db()
        assert regular_user.is_active is False
    #owner can
    def test_user_can_deactive_by_owner(self,url,token_regular_user_client,regular_user):
        response = token_regular_user_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        regular_user.refresh_from_db()
        assert regular_user.is_active is False
    #other users cant
    def test_another_user_can_deactive_user(self,url,token_another_user_client,another_user):
        response = token_another_user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN





@pytest.mark.django_db
class TestAddressListView:
    """
    TEST FOR ADDRESS LIST
    """
    @pytest.fixture
    def address_url(self,admin_user):
        return reverse("accounts:address-list")
    #admin can
    def test_admin_can_view_address_list(self, token_admin_client, admin_user, address_url):
        response = token_admin_client.get(address_url)
        assert response.status_code == status.HTTP_200_OK
    #users cant
    def test_user_can_view_address_list(self, address_url, token_regular_user_client,regular_user):
        response = token_regular_user_client.get(address_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN




@pytest.mark.django_db
class TestAddressDetailView:
    """
    TEST FOR ADDRESS DETAIL
    """
    @pytest.fixture
    def address_detail_url(self,regular_user,address_regular_user):
        return reverse("accounts:address-detail",kwargs={"pk": address_regular_user.pk})
    #admin can
    def test_admin_can_view_address_detail(self, token_admin_client, admin_user, address_detail_url):
        response = token_admin_client.get(address_detail_url)
        assert response.status_code == status.HTTP_200_OK
    #owner can
    def test_user_can_view_address_detail(self, address_detail_url, token_regular_user_client,regular_user):
        response = token_regular_user_client.get(address_detail_url)
        assert response.status_code == status.HTTP_200_OK
    #users cant see another user address
    def test_another_user_view_address_detail_of_others(self, address_detail_url, token_another_user_client,another_user):
        response = token_another_user_client.get(address_detail_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        print(response.data)


@pytest.mark.django_db
class TestAddressUpdateView:
    """
    TEST FOR ADDRESS UPDATE
    """
    @pytest.fixture
    def address_update_url(self,regular_user,address_regular_user):
        return reverse("accounts:address-update",kwargs={"pk": address_regular_user.pk})
    #admin can
    def test_admin_can_update_address(self, token_admin_client, admin_user, address_update_url):
        response = token_admin_client.put(address_update_url)
        assert response.status_code == status.HTTP_200_OK
    #owers can update their own address
    def test_user_can_update_address(self, address_update_url, token_regular_user_client,regular_user):
        response = token_regular_user_client.put(address_update_url)
        assert response.status_code == status.HTTP_200_OK
    #users cant change another user address
    def test_another_user_update_others_address(self, address_update_url, token_another_user_client,another_user):
        response = token_another_user_client.put(address_update_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestChangePasswordView:
    """
    TEST CHANGE PASSWORD
    """
    @pytest.fixture
    def url(self,regular_user):
        return reverse("accounts:change-password")
    #user can change his own password
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
    #user cant change his own password with incorrect password
    def test_user_can_change_own_password_incorrect_old_password(self, token_regular_user_client, regular_user, url):
        data = {
            "old_password": "dfgsdfgsdfg",
            "new_password": "newpassword123",
            "new_password1": "newpassword123",
        }
        response = token_regular_user_client.put(url, data)
        print("Response status:", response.status_code)
        print("Response data:", response.json())
        assert response.status_code == status.HTTP_400_BAD_REQUEST

