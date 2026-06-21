import pytest
from model_bakery import baker
from rest_framework import status

from store.models import Cart, CartItem, Order


@pytest.fixture
def customer(create_customer):
    return create_customer()


@pytest.fixture
def authenticate_customer(api_client, customer):
    api_client.force_authenticate(user=customer.user)
    return customer


@pytest.fixture
def create_order(api_client):
    def do_create_order(cart):
        return api_client.post('/store/orders/', {'cart_id': cart.id})

    return do_create_order


@pytest.mark.django_db
class TestCreateOrder:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post('/store/orders/', {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_cart_id_is_invalid_returns_400(self, authenticate_customer, create_order):
        cart = baker.prepare(Cart, id='00000000-0000-0000-0000-000000000000')

        response = create_order(cart)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['cart_id'] is not None

    def test_if_cart_is_empty_returns_400(self, authenticate_customer, create_order):
        cart = baker.make(Cart)

        response = create_order(cart)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['cart_id'] is not None

    def test_if_cart_has_items_returns_order(self, authenticate_customer, create_order):
        cart = baker.make(Cart)
        cart_item = baker.make(CartItem, cart=cart, quantity=3)

        response = create_order(cart)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] > 0
        assert response.data['customer'] == authenticate_customer.id
        assert response.data['items'][0]['product']['id'] == cart_item.product.id
        assert response.data['items'][0]['quantity'] == 3
        assert not Cart.objects.filter(pk=cart.id).exists()


@pytest.mark.django_db
class TestListOrders:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get('/store/orders/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_only_customer_orders(
        self,
        api_client,
        authenticate_customer,
        create_customer,
    ):
        order = baker.make(Order, customer=authenticate_customer)
        baker.make(Order, customer=create_customer())

        response = api_client.get('/store/orders/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == order.id

    def test_if_user_is_admin_returns_all_orders(self, authenticate, api_client, create_customer):
        authenticate(is_staff=True)
        baker.make(Order, customer=create_customer())
        baker.make(Order, customer=create_customer())

        response = api_client.get('/store/orders/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2


@pytest.mark.django_db
class TestUpdateOrder:
    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_customer):
        order = baker.make(Order, customer=authenticate_customer)

        response = api_client.patch(f'/store/orders/{order.id}/', {'payment_status': Order.PAYMENT_STATUS_COMPLETE})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, authenticate, api_client, create_customer):
        authenticate(is_staff=True)
        order = baker.make(Order, customer=create_customer())

        response = api_client.patch(f'/store/orders/{order.id}/', {'payment_status': Order.PAYMENT_STATUS_COMPLETE})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['payment_status'] == Order.PAYMENT_STATUS_COMPLETE


@pytest.mark.django_db
class TestDeleteOrder:
    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_customer):
        order = baker.make(Order, customer=authenticate_customer)

        response = api_client.delete(f'/store/orders/{order.id}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_204(self, authenticate, api_client, create_customer):
        authenticate(is_staff=True)
        order = baker.make(Order, customer=create_customer())

        response = api_client.delete(f'/store/orders/{order.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Order.objects.filter(pk=order.id).exists()
