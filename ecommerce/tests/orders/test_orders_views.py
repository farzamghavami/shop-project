import pytest
from django.urls import reverse
from rest_framework import status
from decimal import Decimal
from tests.conftest import address


@pytest.mark.django_db
class TestOrderListViews:
    """test order list"""

    @pytest.fixture
    def order_list_url(self):
        return reverse("orders:order-list")

    # test admin just can see all of order_list
    def test_admin_can_see_orders_list(self, token_admin_client, order_list_url, order):
        response = token_admin_client.get(order_list_url)
        assert response.status_code == status.HTTP_200_OK

    # test unauthenticated user cant
    def test_unauthenticated_user_cannot_list_orders(self, client, order_list_url):
        response = client.get(order_list_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # test authenticate user cant
    def test_authenticated_user_cannot_see_others_order(
        self, token_another_user_client, order_list_url, order
    ):
        response = token_another_user_client.get(order_list_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestOrderDetailViews:
    """
    test order detail
    """

    @pytest.fixture
    def order_detail_url(self, order):
        return reverse("orders:order-detail", kwargs={"pk": order.id})

    # test admin user can see order detail
    def test_admin_can_see_order_details(
        self, token_regular_user_client, order_detail_url, order
    ):
        response = token_regular_user_client.get(order_detail_url)
        assert response.status_code == status.HTTP_200_OK

    # test owner user can see order detail
    def test_owner_can_see_order_details(
        self, token_regular_user_client, order_detail_url, order
    ):
        response = token_regular_user_client.get(order_detail_url)
        assert response.status_code == status.HTTP_200_OK

    # test user cant see another user order
    def test_another_user_cant_see_order_details(
        self, token_another_user_client, order_detail_url, order
    ):
        response = token_another_user_client.get(order_detail_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # test unauthenticated user cant see orders
    def test_unauthenticate_user_cant_see_order_details(
        self, client, order_detail_url, order
    ):
        response = client.get(order_detail_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestOrderCreateView:
    """
    test order create
    """

    @pytest.fixture
    def url(self):
        return reverse("orders:order-create")  # آدرس دقیق view

    # test authenticated user can create order
    def test_authenticated_user_can_create_order(
        self, token_regular_user_client, url, product, shop, regular_user, address
    ):
        data = {
            "shop": shop.id,
            "address": address.id,
            "items": [{"product": product.id, "count": 2}],
        }
        response = token_regular_user_client.post(url, data=data, format="json")
        print(response.data)
        print("RESPONSE DATA:", response.data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Decimal(response.data["total_price"]) == Decimal(product.price) * 2
        assert response.data["shop"] == shop.id
        assert response.data["address"] == address.id

    # tset unauthenticated user cant create order
    def test_unauthenticated_user_cannot_create_order(self, client, url):
        response = client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # test user cant create order with invalid data
    def test_invalid_data_returns_400(self, token_regular_user_client, url, shop):
        data = {
            "shop": shop.id,
            "address": "Incomplete data",
            "items": [],  # باید حداقل یک آیتم داشته باشه
        }
        response = token_regular_user_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestOrderUpdateView:
    """
    test order update
    """

    @pytest.fixture
    def url(self, order):
        return reverse("orders:order-update", kwargs={"pk": order.id})

    # tset owner can update his order
    def test_owner_can_update_order(
        self, token_regular_user_client, order, url, address
    ):
        response = token_regular_user_client.put(url, data={"address": address.id})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["address"] == address.id

    # test authenticated user cant update another user order
    def test_authenticated_user_cannot_update_order(
        self, token_another_user_client, order, url,address
    ):
        response = token_another_user_client.put(url, data={"address":address.id  })
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # test admin can update user order
    def test_admin_can_update_order(self, token_admin_client, order, url, address):
        response = token_admin_client.put(url, data={"address": address.id})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["address"] == address.id


@pytest.mark.django_db
class TestOrderDeleteView:
    """
    test order delete
    """

    @pytest.fixture
    def url(self, order):
        return reverse("orders:order-delete", kwargs={"pk": order.id})

    # test owner can delete his order
    def test_owner_can_delete_order(self, token_regular_user_client, order, url):
        response = token_regular_user_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    # test authenticated user cany delete another user order
    def test_authenticated_user_can_delete_order(
        self, token_another_user_client, order, url
    ):
        response = token_another_user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # test unauthenticated user cant
    def test_unauthenticated_user_cannot_delete_order(self, client, url):
        response = client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # test admin can delete user order
    def test_admin_can_delete_order(self, token_admin_client, order, url):
        response = token_admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestOrderItemListView:
    @pytest.fixture
    def url(self):
        return reverse("orders:orderitem-list")

    def test_authenticate_user_cannot_see_orderitem_list(
        self, token_regular_user_client, url
    ):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_see_orderitem_list(self, token_admin_client, order, url):
        response = token_admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_unauthenticated_user_cannot_see_orderitem_list(self, client, url):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestOrderItemDetailView:
    """
    test order item detail
    """

    @pytest.fixture
    def url(self, order_item):
        return reverse("orders:orderitem-detail", kwargs={"pk": order_item.id})

    # test admin can view user order_item
    def test_admin_can_view_order_item_detail(
        self, token_admin_client, url, order_item
    ):
        response = token_admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data

    # test unauthenticated user cant view other user order_item
    def test_unauthenticated_user_cannot_view_order_item_detail(
        self, client, order_item, url
    ):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # test authenticated user cant
    def test_authenticated_user_cannot_view_order_item_detail(
        self, token_another_user_client, order_item, url
    ):
        response = token_another_user_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # test owner can get view his order_item
    def test_owner_can_view_order_item_detail(
        self, token_regular_user_client, order_item, url
    ):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestOrderItemUpdateView:
    """
    test order item update
    """

    @pytest.fixture
    def url(self, order_item):
        return reverse("orders:orderitem-update", kwargs={"pk": order_item.id})

    # test owner user can update his order_item
    def test_owner_user_can_update_order_item(
        self, token_regular_user_client, order_item, url, address
    ):
        response = token_regular_user_client.put(url, data={"count": 5})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 5

    # test admin can see user order_item
    def test_admin_can_update_order_item(
        self, token_admin_client, order_item, url, address
    ):
        response = token_admin_client.put(url, data={"count": 5})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 5

    # test unauthenticated user cant
    def test_unauthenticated_user_cannot_update_order_item(
        self, client, order_item, url
    ):
        response = client.put(url, data={"count": 5})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # test user cant update another user order_item
    def test_authenticated_user_cannot_update_order_item(
        self, token_another_user_client, order_item, url, address
    ):
        response = token_another_user_client.put(url, data={"count": 5})
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestOrderItemDeleteView:
    """
    test order item delete
    """

    @pytest.fixture
    def url(self, order_item):
        return reverse("orders:orderitem-delete", kwargs={"pk": order_item.id})

    # test user can delete his order_item
    def test_owner_can_delete_order_item(
        self, token_regular_user_client, order_item, url
    ):
        response = token_regular_user_client.delete(url)
        assert response.status_code == status.HTTP_200_OK

    # test admin can delete user order_item
    def test_admin_can_delete_order_item(self, token_admin_client, order_item, url):
        response = token_admin_client.delete(url)
        assert response.status_code == status.HTTP_200_OK

    # test unauthenticated user cant
    def test_unauthenticated_user_cannot_delete_order_item(
        self, client, order_item, url
    ):
        response = client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # test user cant delete other user order_item
    def test_authenticated_user_cannot_delete_order_item(
        self, token_another_user_client, order_item, url
    ):
        response = token_another_user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestDeliveryListView:
    """
    test delivery list
    """

    @pytest.fixture
    def url(self):
        return reverse("orders:delivery-list")

    # test authenticated user can see delivery_list
    def test_authenticated_user_can_view_delivery_list(
        self, token_regular_user_client, url
    ):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    # test unauthenticated user cant
    def test_unauthenticated_user_cannot_view_delivery_list(self, client, url):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # test admin can
    def test_admin_can_view_delivery_list(self, token_admin_client, url):
        response = token_admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeliveryDetailView:
    """
    test delivery detail
    """

    @pytest.fixture
    def url(self, delivery):
        return reverse("orders:delivery-detail", kwargs={"pk": delivery.id})

    # test authenticated user can see delivery method
    def test_authenticated_user_can_view_delivery_detail(
        self, token_regular_user_client, delivery, url
    ):
        response = token_regular_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    # test unauthenticated user cant
    def test_unauthenticated_user_cannot_view_delivery_detail(
        self, client, delivery, url
    ):
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestDeliveryCreateView:
    """
    test delivery create
    """

    @pytest.fixture
    def url(self):
        return reverse("orders:delivery-create")

    # test admin can create delivery method
    def test_admin_can_create_delivery_method(
        self, token_admin_client, delivery, url, order
    ):
        data = {
            "order": order.id,
            "method": "TPOX",
        }

        response = token_admin_client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED

    # test unauthenticated user cant
    def test_unauthenticated_user_cannot_create_delivery_method(
        self, client, delivery, url, order
    ):

        data = {
            "order": order.id,
            "method": "TPOX",
        }
        response = client.post(url, data=data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # test authenticated user cant
    def test_authenticated_user_cannot_create_delivery_method(
        self, token_another_user_client, url, order
    ):
        data = {
            "order": order.id,
            "method": "TPOX",
        }
        response = token_another_user_client.post(url, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestDeliveryDeleteView:
    """
    test delivery delete
    """

    @pytest.fixture
    def url(self, delivery):
        return reverse("orders:delivery-delete", kwargs={"pk": delivery.id})

    # test admin can delete delivery method
    def test_admin_can_delete_delivery_method(self, token_admin_client, delivery, url):
        response = token_admin_client.delete(url)
        assert response.status_code == status.HTTP_200_OK

    # test unauthenticated user cant
    def test_unauthenticated_user_cannot_delete_delivery_method(
        self, client, delivery, url
    ):
        response = client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # test authenticated user cant
    def test_authenticated_user_cannot_delete_delivery_method(
        self, token_regular_user_client, delivery, url
    ):
        response = token_regular_user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
