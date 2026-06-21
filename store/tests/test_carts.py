import pytest
from model_bakery import baker
from rest_framework import status

from store.models import Cart, CartItem, Product


@pytest.fixture
def create_cart(api_client):
    def do_create_cart():
        return api_client.post('/store/carts/')

    return do_create_cart


@pytest.fixture
def create_cart_item(api_client):
    def do_create_cart_item(cart, cart_item):
        return api_client.post(f'/store/carts/{cart.id}/items/', cart_item)

    return do_create_cart_item


@pytest.mark.django_db
class TestCreateCart:
    def test_returns_201(self, create_cart):
        response = create_cart()

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] is not None


@pytest.mark.django_db
class TestRetrieveCart:
    def test_if_cart_exists_returns_200(self, api_client):
        cart = baker.make(Cart)
        item = baker.make(CartItem, cart=cart, quantity=2)

        response = api_client.get(f'/store/carts/{cart.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == str(cart.id)
        assert response.data['items'][0]['id'] == item.id
        assert response.data['total_price'] == item.quantity * item.product.unit_price

    def test_if_cart_does_not_exist_returns_404(self, api_client):
        response = api_client.get('/store/carts/00000000-0000-0000-0000-000000000000/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteCart:
    def test_if_cart_exists_returns_204(self, api_client):
        cart = baker.make(Cart)

        response = api_client.delete(f'/store/carts/{cart.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestCreateCartItem:
    def test_if_product_id_is_invalid_returns_400(self, create_cart_item):
        cart = baker.make(Cart)

        response = create_cart_item(cart, {'product_id': 999, 'quantity': 1})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['product_id'] is not None

    def test_if_data_is_valid_returns_201(self, create_cart_item):
        cart = baker.make(Cart)
        product = baker.make(Product)

        response = create_cart_item(cart, {'product_id': product.id, 'quantity': 2})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
        assert response.data['product_id'] == product.id
        assert response.data['quantity'] == 2

    def test_if_product_already_in_cart_updates_quantity(self, create_cart_item):
        cart = baker.make(Cart)
        cart_item = baker.make(CartItem, cart=cart, quantity=2)

        response = create_cart_item(cart, {'product_id': cart_item.product.id, 'quantity': 3})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] == cart_item.id
        assert response.data['quantity'] == 5


@pytest.mark.django_db
class TestUpdateCartItem:
    def test_if_item_exists_returns_200(self, api_client):
        cart_item = baker.make(CartItem, quantity=1)

        response = api_client.patch(
            f'/store/carts/{cart_item.cart.id}/items/{cart_item.id}/',
            {'quantity': 4},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['quantity'] == 4

    def test_if_quantity_is_invalid_returns_400(self, api_client):
        cart_item = baker.make(CartItem, quantity=1)

        response = api_client.patch(
            f'/store/carts/{cart_item.cart.id}/items/{cart_item.id}/',
            {'quantity': 0},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['quantity'] is not None


@pytest.mark.django_db
class TestDeleteCartItem:
    def test_if_item_exists_returns_204(self, api_client):
        cart_item = baker.make(CartItem)

        response = api_client.delete(f'/store/carts/{cart_item.cart.id}/items/{cart_item.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
