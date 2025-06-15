import pytest
from orders.models import OrderItem, Delivery


@pytest.mark.django_db
class TestOrderModel:
    """
    test orders model
    """

    def test_order_create(self, order, shop, regular_user, address):
        order = order
        assert order.shop == shop
        assert order.user == regular_user
        assert order.address == address
        assert order.total_price == 100


@pytest.mark.django_db
class TestOrderItemModel:
    """
    test orderitem model
    """

    def test_order_item_create(self, order, product):
        orderitem = OrderItem.objects.create(
            order=order, product=product, row_price=100, count=2
        )
        assert orderitem.order == order
        assert orderitem.product == product
        assert orderitem.row_price == 100
        assert orderitem.count == 2


@pytest.mark.django_db
class TestDeliveryModel:
    """
    test delivery model
    """

    def test_delivery_create(self, order):
        delivery = Delivery.objects.create(order=order, method="TPOX")
        assert delivery.method == "TPOX"
        assert delivery.order == order
