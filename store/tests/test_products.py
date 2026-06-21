from decimal import Decimal

import pytest
from model_bakery import baker
from rest_framework import status

from store.models import Collection, OrderItem, Product


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/', product)

    return do_create_product


@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_returns_401(self, create_product):
        response = create_product({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_product):
        authenticate()

        response = create_product({})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_product):
        authenticate(is_staff=True)

        response = create_product({
            'title': '',
            'slug': '',
            'unit_price': 0,
            'inventory': 0,
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        assert response.data['unit_price'] is not None
        assert response.data['inventory'] is not None

    def test_if_data_is_valid_returns_201(self, authenticate, create_product):
        authenticate(is_staff=True)
        collection = baker.make(Collection)

        response = create_product({
            'title': 'Coffee',
            'slug': 'coffee',
            'unit_price': '9.99',
            'inventory': 12,
            'collection': collection.id,
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
        assert response.data['title'] == 'Coffee'


@pytest.mark.django_db
class TestRetrieveProduct:
    def test_if_product_exists_returns_200(self, api_client):
        product = baker.make(Product, unit_price=Decimal('10.00'))

        response = api_client.get(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == product.id
        assert response.data['title'] == product.title
        assert response.data['price_with_tax'] == product.unit_price * Decimal(1.1)

    def test_if_product_does_not_exist_returns_404(self, api_client):
        response = api_client.get('/store/products/999/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestListProducts:
    def test_returns_products(self, api_client):
        product = baker.make(Product)

        response = api_client.get('/store/products/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['id'] == product.id

    def test_can_filter_by_collection(self, api_client):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        baker.make(Product)

        response = api_client.get(f'/store/products/?collection_id={collection.id}')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['id'] == product.id


@pytest.mark.django_db
class TestDeleteProduct:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        product = baker.make(Product)

        response = api_client.delete(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, api_client):
        authenticate()
        product = baker.make(Product)

        response = api_client.delete(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_has_order_item_returns_405(self, authenticate, api_client, create_customer):
        authenticate(is_staff=True)
        order_item = baker.make(OrderItem, order__customer=create_customer())

        response = api_client.delete(f'/store/products/{order_item.product.id}/')

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_if_product_has_no_order_item_returns_204(self, authenticate, api_client):
        authenticate(is_staff=True)
        product = baker.make(Product)

        response = api_client.delete(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
