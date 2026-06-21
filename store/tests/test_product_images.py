import pytest
from model_bakery import baker
from rest_framework import status

from store.models import Product, ProductImage


@pytest.mark.django_db
class TestListProductImages:
    def test_returns_images_for_product(self, api_client):
        product = baker.make(Product)
        image = baker.make(ProductImage, product=product, image='store/images/test.jpg')
        baker.make(ProductImage, image='store/images/other.jpg')

        response = api_client.get(f'/store/products/{product.id}/images/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == image.id


@pytest.mark.django_db
class TestRetrieveProductImage:
    def test_if_image_exists_returns_200(self, api_client):
        image = baker.make(ProductImage, image='store/images/test.jpg')

        response = api_client.get(f'/store/products/{image.product.id}/images/{image.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == image.id


@pytest.mark.django_db
class TestDeleteProductImage:
    def test_if_image_exists_returns_204(self, api_client):
        image = baker.make(ProductImage, image='store/images/test.jpg')

        response = api_client.delete(f'/store/products/{image.product.id}/images/{image.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ProductImage.objects.filter(pk=image.id).exists()
