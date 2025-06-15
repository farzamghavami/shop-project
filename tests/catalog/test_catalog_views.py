import pytest
from django.urls import reverse
from rest_framework import status
from catalog.models import Shop, Category, Wishlist, Product

from tests.conftest import (
    product_seller_user,
    shop_seller_user,
    token_admin_client,
    regular_user,
)


@pytest.mark.django_db
class TestProductListView:
    """
    test product list view
    """

    @pytest.fixture
    def url(self):
        return reverse("catalog:product-list")

    # test authenticated user can
    def test_authenticated_user_can_see_product_list(
        self,
        token_regular_user_client,
        url,
    ):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    # test unauthenticated user cant
    def test_unauthenticated_user_cannot_see_product_list(self, client, url):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestProductDetailView:
    """
    test product detail view
    """

    @pytest.fixture
    def url(self, product):
        return reverse("catalog:product-detail", kwargs={"pk": product.pk})

    # test authenticated user can
    def test_authenticated_user_can_see_product_detail(
        self, token_another_user_client, url, product
    ):
        response = token_another_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == product.name
        assert response.data["id"] == product.id

    # test unauthenticated user cant
    def test_unauthenticated_user_cannot_see_product_detail(self, client, url):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # test with no product
    def test_return_404_if_product_not_found(self, token_another_user_client, url):
        url = reverse("catalog:product-detail", kwargs={"pk": 999})
        response = token_another_user_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestProductCreateView:
    """
    test product create
    """

    @pytest.fixture
    def url(self, product):
        return reverse("catalog:product-create")

    # admin can create product
    def test_admin_can_create_product(self, token_admin_client, url, shop, category):
        data = {
            "shop": shop.id,
            "category": category.id,
            "name": "test",
            "description": "test",
            "image_url": "test",
            "price": 100,
            "is_active": True,
        }
        response = token_admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    # seler can create product
    def test_seller_can_create_product(
        self, token_seller_user_client, url, shop, category
    ):
        data = {
            "shop": shop.id,
            "category": category.id,
            "name": "test",
            "description": "test",
            "image_url": "test",
            "price": 200,
            "is_active": True,
        }
        response = token_seller_user_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    # test regular user cant create product
    def test_regular_user_cannot_create_product(
        self, token_regular_user_client, url, shop, category
    ):
        data = {
            "shop": shop.id,
            "category": category.id,
            "name": "test",
            "description": "test",
            "image_url": "test",
            "price": 200,
            "is_active": True,
        }
        response = token_regular_user_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # test create with invalid product
    def test_invalid_product_data(self, token_seller_user_client, url):
        data = {
            "name": "test",
            "description": "test",
        }
        response = token_seller_user_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestProductUpdateView:
    """
    test product update
    """

    @pytest.fixture
    def url(self, product, product_seller_user):
        return reverse("catalog:product-update", kwargs={"pk": product_seller_user.pk})

    # test admin can update product
    def test_admin_can_update_product(
        self, token_admin_client, url, product_seller_user
    ):
        data = {
            "name": "test3",
        }
        response = token_admin_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        product_seller_user.refresh_from_db()
        assert product_seller_user.name == "test3"

    # test seller can update own product
    def test_seller_can_update_own_product(
        self,
        token_seller_user_client,
        url,
        product_seller_user,
    ):
        data = {
            "name": "test2",
        }
        response = token_seller_user_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        product_seller_user.refresh_from_db()
        assert product_seller_user.name == "test2"

    # test another seller cant update other sellers product
    def test_another_seller_can_update_other_seller_product(
        self, token_seller2_user_client, url, product_seller_user
    ):
        data = {
            "name": "test3",
        }
        response = token_seller2_user_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestProductDeleteView:
    """
    test product delete
    """

    @pytest.fixture
    def url(self, product, product_seller_user):
        return reverse("catalog:product-delete", kwargs={"pk": product_seller_user.pk})

    # test admin can delet product
    def test_admin_can_delete_product(
        self, token_admin_client, url, product, product_seller_user
    ):
        response = token_admin_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        product_seller_user.refresh_from_db()
        assert product_seller_user.is_active is False

    # test seller can delete own product
    def test_seller_can_delete_own_product(
        self, token_seller_user_client, url, product, product_seller_user
    ):
        response = token_seller_user_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        product_seller_user.refresh_from_db()
        assert product_seller_user.is_active is False

    # test seller cant delete others product
    def test_another_seller_can_delete_other_seller_product(
        self, token_seller2_user_client, url, product_seller_user
    ):
        response = token_seller2_user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert product_seller_user.is_active is True


@pytest.mark.django_db
class TestShopListview:
    """
    test shop list view
    """

    @pytest.fixture
    def url(
        self,
        shop,
    ):
        return reverse("catalog:shop-list")

    # test authenticated user can view shop lists
    def test_authenticated_user_can_view_shop_list(
        self, token_regular_user_client, shop, url
    ):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data

    # test unauthenticated users cant see shop lists
    def test_unauthenticated_user_can_view_shop_list(self, client, shop, url):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestShopDetailView:
    """
    test shop detail
    """

    @pytest.fixture
    def url(self, shop):
        return reverse("catalog:shop-detail", kwargs={"pk": shop.pk})

    # test authenticated user can view shop detail
    def test_authenticated_user_can_view_shop_detail(
        self, token_regular_user_client, shop, url
    ):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    # test unauthenticated user cant see shop detail
    def test_unauthenticated_user_can_view_shop_detail(self, client, shop, url):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestShopCreateView:
    """
    test shop create
    """

    @pytest.fixture
    def url(self, shop):
        return reverse("catalog:shop-create")

    @pytest.fixture
    def valid_shop_data(self, address):
        return {"name": "Test Shop", "address": address.id}

    # test admin can create shop
    def test_admin_can_create_shop(
        self, token_admin_client, shop, url, address, seller_user, valid_shop_data
    ):
        response = token_admin_client.post(url, data=valid_shop_data)
        assert response.status_code == status.HTTP_201_CREATED

    # test seller can create shop
    def test_seller_can_create_shop(
        self, token_seller_user_client, shop, url, address, valid_shop_data
    ):
        response = token_seller_user_client.post(url, data=valid_shop_data)
        assert response.status_code == status.HTTP_201_CREATED

    # test regular user cannot create shop
    def test_regular_user_cannot_create_shop(
        self, token_regular_user_client, shop, url, address, valid_shop_data
    ):
        response = token_regular_user_client.post(url, data=valid_shop_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # test unauthenticated user cannot create shop
    def test_unauthenticated_user_cannot_create_shop(
        self, client, shop, url, address, valid_shop_data
    ):
        response = client.post(url, data=valid_shop_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestShopUpdateView:
    """
    test shop update
    """

    @pytest.fixture
    def url(self, shop_seller_user):
        return reverse("catalog:shop-update", kwargs={"pk": shop_seller_user.pk})

    # test admin can update all shops
    def test_admin_can_update_shop(self, token_admin_client, url, shop_seller_user):
        data = {
            "name": "admin update name",
        }
        response = token_admin_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        shop_seller_user.refresh_from_db()
        assert shop_seller_user.name == "admin update name"

    # test seller can update his own shop
    def test_owner_can_update_shop(
        self, token_seller_user_client, url, shop_seller_user
    ):
        data = {
            "name": "owner update name",
        }
        response = token_seller_user_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        shop_seller_user.refresh_from_db()
        assert shop_seller_user.name == "owner update name"

    # test seller cant update others shop
    def test_another_seller_can_update_shop(
        self, token_seller2_user_client, url, shop_seller_user
    ):
        data = {
            "name": "another owner update name",
        }
        response = token_seller2_user_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestShopDeleteView:
    """
    test shop delete
    """

    @pytest.fixture
    def url(self, shop_seller_user):
        return reverse("catalog:shop-delete", kwargs={"pk": shop_seller_user.id})

    # test admin can delete shop
    def test_admin_can_delete_shop(self, token_admin_client, url, shop_seller_user):
        response = token_admin_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        shop_seller_user.refresh_from_db()
        assert shop_seller_user.is_active is False

    # test owner seller can delete his shop
    def test_owner_can_delete_shop(
        self, token_seller_user_client, url, shop_seller_user
    ):
        response = token_seller_user_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        shop_seller_user.refresh_from_db()
        assert shop_seller_user.is_active is False

    # test seller cant delete another seller shop
    def test_another_seller_can_delete_shop(
        self, token_seller2_user_client, url, shop_seller_user
    ):
        response = token_seller2_user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestCategoryListView:
    """
    test category list
    """

    @pytest.fixture
    def url(self, shop):
        return reverse("catalog:category-list")

    # test authenticated user can view
    def test_authenticated_user_can_view_categories(
        self,
        token_regular_user_client,
        url,
    ):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    # test unauthenticated user cant
    def test_unauthenticated_user_cant_view_categories(
        self,
        client,
        url,
    ):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCategoryDetailView:
    """
    test category detail
    """

    @pytest.fixture
    def url(self, category):
        return reverse("catalog:category-detail", kwargs={"pk": category.id})

    # test authenticated user can view
    def test_authenticated_user_can_view_category_detail(
        self,
        token_regular_user_client,
        category,
        url,
    ):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        category.refresh_from_db()
        assert category.name == category.name

    # test unauthenticated user cant view
    def test_unauthenticated_user_cant_view_category_detail(
        self,
        client,
        url,
    ):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCreateCategoryView:
    """
    test create category
    """

    @pytest.fixture
    def url(self, category):
        return reverse("catalog:category-create")

    # test admin can create category with no parent
    def test_admin_can_create_category_without_parent(self, token_admin_client, url):
        data = {"name": "Electronic"}
        response = token_admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Electronic"
        assert Category.objects.filter(name="Electronic").exists()

    # test admin can create category with parent
    def test_admin_can_create_category_with_parent(self, token_admin_client, url):
        parent = Category.objects.create(name="Electronic")
        data = {"name": "labtops", "parent": parent.id}
        response = token_admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "labtops"
        assert response.data["parent"]["id"] == parent.id

    # test regular user cant create category
    def test_regular_user_cant_create_category(self, token_regular_user_client, url):
        data = {"name": "Electronic"}
        response = token_regular_user_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # test create category with invalid data
    def test_invalid_data_returns_400(self, token_admin_client, url):

        data = {"parent": ""}
        response = token_admin_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # test unauthenticated user cant
    def test_unauthenticated_user_can_view_category(
        self,
        client,
        url,
    ):
        data = {"name": "Electronic"}
        response = client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCategoryUpdateView:
    """
    test category update
    """

    @pytest.fixture
    def url(self, category):
        return reverse("catalog:category-update", kwargs={"pk": category.id})

    # test admin can update category
    def test_admin_can_update_category(
        self,
        token_admin_client,
        category,
        url,
    ):
        data = {
            "name": "admin updated",
        }
        response = token_admin_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        category.refresh_from_db()
        assert category.name == "admin updated"

    # test regular user cant update category
    def test_regular_user_cant_update_category(
        self,
        token_regular_user_client,
        category,
        url,
    ):
        data = {
            "name": "regular user updated",
        }
        response = token_regular_user_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # test unauthenticated user cant update category
    def test_unauthenticated_user_cant_update_category(
        self,
        client,
        url,
    ):

        data = {
            "name": "unauthenticate user updated",
        }
        response = client.put(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCategoryDeleteView:
    """
    test category delete
    """

    @pytest.fixture
    def url(self, category):
        return reverse("catalog:category-delete", kwargs={"pk": category.id})

    # test admin can delete category
    def test_admin_can_delete_category(
        self,
        token_admin_client,
        url,
        category,
    ):
        assert category.is_active is True
        response = token_admin_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        category.refresh_from_db()
        assert category.is_active is False

    # test regular user cant delete category
    def test_regular_user_cannot_delete_category(
        self, token_regular_user_client, category, url
    ):
        response = token_regular_user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # test unauthenticated user cant delete category
    def test_unauthenticated_user_cant_delete_category(
        self,
        client,
        url,
    ):
        response = client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # test admin cant delete category with no pk
    def test_delete_nonexistent_category_returns_404(self, token_admin_client):
        url = reverse("catalog:category-delete", kwargs={"pk": 9999})
        response = token_admin_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestWishListCreateView:
    """
    test wishlist creation
    """

    @pytest.fixture
    def url(
        self,
    ):
        return reverse("catalog:wishlist-create")

    # test authenticated user can create wish_list
    def test_authenticated_user_can_create_wishlist(
        self,
        token_regular_user_client,
        url,
        product,
        shop,
        category,
    ):
        data = {
            "product": product.id,
        }
        response = token_regular_user_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["product"]["id"] == product.id

    # test unauthenticated user cant
    def test_unauthenticated_user_cant_create_wishlist(
        self,
        client,
        url,
        product,
    ):
        data = {"product": product.id}
        response = client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # test admin can create
    def test_admin_can_create_wishlist(self, token_admin_client, url, product):
        data = {"product": product.id}
        response = token_admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["product"]["id"] == product.id


@pytest.mark.django_db
class TestWishlistDetailView:
    """
    test wishlist detail
    """

    @pytest.fixture
    def url(self, regular_user, product):
        wishlist = Wishlist.objects.create(user=regular_user, product=product)
        return reverse("catalog:wishlist-detail", kwargs={"pk": wishlist.id})

    # tset authenticated user can
    def test_authenticated_user_can_detail_wishlist(
        self, token_regular_user_client, regular_user, product, url
    ):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "product" in response.data
        assert "id" in response.data["product"]
        assert "user" in response.data

    # test unauthenticated user cant
    def test_unauthenticated_user_cant_detail_wishlist(
        self, client, regular_user, product, url
    ):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestWishListDeleteView:
    """
    test wishlist delete
    """

    @pytest.fixture
    def wishlist(self, regular_user, product):
        wishlist = Wishlist.objects.create(user=regular_user, product=product)
        return wishlist

    @pytest.fixture
    def url(self, regular_user, product, wishlist):
        return reverse("catalog:wishlist-delete", kwargs={"pk": wishlist.id})

    # test admin can delete wish_list
    def test_admin_can_delete_wishlist(
        self, token_admin_client, regular_user, product, url
    ):
        response = token_admin_client.delete(url)
        assert response.status_code == status.HTTP_200_OK

    # test owner can delete wish_list
    def test_owner_can_delete_wishlist(
        self, token_regular_user_client, regular_user, product, url, wishlist
    ):
        response = token_regular_user_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        wishlist.refresh_from_db()
        assert wishlist.is_active is False

    # users cant delete others wish_list
    def test_user_can_delete_other_wishlist(
        self,
        token_another_user_client,
        url,
    ):
        response = token_another_user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
