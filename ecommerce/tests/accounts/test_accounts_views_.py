from http.client import responses

import pytest
from django.db.models.expressions import result
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from tests.conftest import token_admin_client, regular_user

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
        assert response.data["email"] == regular_user.email

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

    def test_admin_can_delete_user_detail(self, token_admin_client, admin_user, regular_user,url):
        response = token_admin_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        regular_user.refresh_from_db()
        assert regular_user.is_active is False

    def test_user_can_delete_by_owner(self,url,token_regular_user_client,regular_user):
        response = token_regular_user_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        regular_user.refresh_from_db()
        assert regular_user.is_active is False

    def test_another_user_can_delete_user(self,url,token_another_user_client,another_user):
        response = token_another_user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
