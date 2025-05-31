import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestProductListView:

    @pytest.fixture
    def url(self):
        return reverse("catalog:product-list")  # اطمینان حاصل کن که این نام در urls.py تعریف شده


    def test_authenticated_user_can_see_product_list(self, token_regular_user_client, url,):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_unauthenticated_user_cannot_see_product_list(self, client, url):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestProductDetailView:
    @pytest.fixture
    def url(self, product):
        return reverse("catalog:product-detail", kwargs={"pk":product.pk})

    def test_authenticated_user_can_see_product_detail(self, token_another_user_client, url,product):
        response = token_another_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == product.name
        assert response.data["id"] == product.id

    def test_unauthenticated_user_cannot_see_product_detail(self, client, url):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_return_404_if_product_not_found(self, token_another_user_client, url):
        url = reverse("catalog:product-detail", kwargs={"pk": 999})
        response = token_another_user_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

