import pytest
from model_bakery import baker
from rest_framework import status

from store.models import Product, Review


@pytest.fixture
def create_review(api_client):
    def do_create_review(product, review):
        return api_client.post(f'/store/products/{product.id}/reviews/', review)

    return do_create_review


@pytest.mark.django_db
class TestCreateReview:
    def test_if_data_is_invalid_returns_400(self, create_review):
        product = baker.make(Product)

        response = create_review(product, {'name': '', 'description': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None
        assert response.data['description'] is not None

    def test_if_data_is_valid_returns_201(self, create_review):
        product = baker.make(Product)

        response = create_review(product, {'name': 'Alice', 'description': 'Great.'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
        assert response.data['name'] == 'Alice'


@pytest.mark.django_db
class TestListReviews:
    def test_returns_reviews_for_product(self, api_client):
        product = baker.make(Product)
        review = baker.make(Review, product=product)
        baker.make(Review)

        response = api_client.get(f'/store/products/{product.id}/reviews/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == review.id


@pytest.mark.django_db
class TestDeleteReview:
    def test_if_review_exists_returns_204(self, api_client):
        review = baker.make(Review)

        response = api_client.delete(f'/store/products/{review.product.id}/reviews/{review.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
