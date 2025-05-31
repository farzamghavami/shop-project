import pytest
from django.urls import reverse
from rest_framework import status
from catalog.models import Shop

from tests.conftest import product_seller_user, shop_seller_user


@pytest.mark.django_db
class TestProductListView:

    @pytest.fixture
    def url(self):
        return reverse("catalog:product-list")  # اطمینان حاصل کن که این نام در urls.py تعریف شده

    def test_authenticated_user_can_see_product_list(self, token_regular_user_client, url, ):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_unauthenticated_user_cannot_see_product_list(self, client, url):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestProductDetailView:
    @pytest.fixture
    def url(self, product):
        return reverse("catalog:product-detail", kwargs={"pk": product.pk})

    def test_authenticated_user_can_see_product_detail(self, token_another_user_client, url, product):
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


@pytest.mark.django_db
class TestProductCreateView:
    @pytest.fixture
    def url(self, product):
        return reverse("catalog:product-create")

    def test_admin_can_create_product(self, token_admin_client, url, shop, category):
        data = {
            "shop": shop.id,
            "category": category.id,
            "name": "test",
            "description": "test",
            "image_url": "test",
            "price": 100,
            "is_active": True
        }
        response = token_admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_seller_can_create_product(self, token_seller_user_client, url, shop, category):
        data = {
            "shop": shop.id,
            "category": category.id,
            "name": "test",
            "description": "test",
            "image_url": "test",
            "price": 200,
            "is_active": True
        }
        response = token_seller_user_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_regular_user_can_create_product(self, token_regular_user_client, url, shop, category):
        data = {
            "shop": shop.id,
            "category": category.id,
            "name": "test",
            "description": "test",
            "image_url": "test",
            "price": 200,
            "is_active": True
        }
        response = token_regular_user_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_invalid_product_data(self, token_seller_user_client, url):
        data = {
            "name": "test",
            "description": "test",
        }
        response = token_seller_user_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestProductUpdateView:
    @pytest.fixture
    def url(self, product, product_seller_user):
        return reverse("catalog:product-update", kwargs={"pk": product_seller_user.pk})

    def test_admin_can_update_product(self, token_admin_client, url,product_seller_user):
        data = {
            "name": "test3",
        }
        response = token_admin_client.put(url,data)
        assert response.status_code == status.HTTP_200_OK
        product_seller_user.refresh_from_db()
        assert product_seller_user.name == "test3"


    def test_seller_can_update_own_product(self, token_seller_user_client, url, product_seller_user,):
        data = {
            "name": "test2",
        }
        response = token_seller_user_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        product_seller_user.refresh_from_db()
        assert product_seller_user.name == "test2"

    def test_another_seller_can_update_other_seller_product(self, token_seller2_user_client, url, product_seller_user):
        data = {
            "name": "test3",
        }
        response = token_seller2_user_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestProductDeleteView:
    @pytest.fixture
    def url(self,product, product_seller_user):
        return reverse("catalog:product-delete", kwargs={"pk": product_seller_user.pk})

    def test_admin_can_delete_product(self, token_admin_client, url, product, product_seller_user):
        response = token_admin_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        product_seller_user.refresh_from_db()
        assert product_seller_user.is_active is False

    def test_seller_can_delete_own_product(self, token_seller_user_client, url, product, product_seller_user):
        response = token_seller_user_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        product_seller_user.refresh_from_db()
        assert product_seller_user.is_active is False

    def test_another_seller_can_delete_other_seller_product(self, token_seller2_user_client, url, product_seller_user):
        response = token_seller2_user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert product_seller_user.is_active is True


@pytest.mark.django_db
class TestShopListview:
    @pytest.fixture
    def url(self, shop,):
        return reverse("catalog:shop-list")

    def test_authenticated_user_can_view_shop_list(self, token_regular_user_client, shop, url):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_unauthenticated_user_can_view_shop_list(self, client, shop, url):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestShopDetailView:
    @pytest.fixture
    def url(self, shop):
        return reverse("catalog:shop-detail", kwargs={"pk": shop.pk})

    def test_authenticated_user_can_view_shop_detail(self, token_regular_user_client, shop, url):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_unauthenticated_user_can_view_shop_detail(self, client, shop, url):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestShopCreateView:
    @pytest.fixture
    def url(self, shop):
        return reverse("catalog:shop-create")
    @pytest.fixture
    def valid_shop_data(self, address):
        return {
            "name": "Test Shop",
            "address": address.id
        }

    def test_admin_can_create_shop(self, token_admin_client, shop, url,address,seller_user,valid_shop_data):
        response = token_admin_client.post(url, data= valid_shop_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_seller_can_create_shop(self,token_seller_user_client, shop, url,address,valid_shop_data):
        response = token_seller_user_client.post(url, data= valid_shop_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_regular_user_can_create_shop(self, token_regular_user_client, shop, url,address,valid_shop_data):
        response = token_regular_user_client.post(url, data= valid_shop_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_user_can_create_shop(self, client, shop, url,address,valid_shop_data):
        response = client.post(url, data= valid_shop_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestShopUpdateView:
    @pytest.fixture
    def url(self, shop_seller_user):
        return reverse("catalog:shop-update", kwargs={"pk": shop_seller_user.pk})

    def test_admin_can_update_shop(self, token_admin_client, url,shop_seller_user):
        data = {
            "name": "admin update name",
        }
        response = token_admin_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        shop_seller_user.refresh_from_db()
        assert shop_seller_user.name == "admin update name"

    def test_owner_can_update_shop(self, token_seller_user_client, url, shop_seller_user):
        data = {
            "name": "owner update name",
        }
        response = token_seller_user_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        shop_seller_user.refresh_from_db()
        assert shop_seller_user.name == "owner update name"

    def test_another_seller_can_update_shop(self, token_seller2_user_client, url, shop_seller_user):
        data = {
            "name": "another owner update name",
        }
        response = token_seller2_user_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestShopDeleteView:
    @pytest.fixture
    def url(self, shop_seller_user):
        return reverse("catalog:shop-delete", kwargs={"pk": shop_seller_user.id})

    def test_admin_can_delete_shop(self, token_admin_client, url, shop_seller_user):
        response = token_admin_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        shop_seller_user.refresh_from_db()
        assert shop_seller_user.is_active is False

    def test_owner_can_delete_shop(self, token_seller_user_client, url, shop_seller_user):
        response = token_seller_user_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        shop_seller_user.refresh_from_db()
        assert shop_seller_user.is_active is False

    def test_another_seller_can_delete_shop(self, token_seller2_user_client, url, shop_seller_user):
        response = token_seller2_user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestCategoryListView:
    @pytest.fixture
    def url(self,shop):
        return reverse("catalog:category-list")

    def test_authenticated_user_can_view_categories(self,token_regular_user_client,url,):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_unauthenticated_user_can_view_categories(self,client,url,):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

