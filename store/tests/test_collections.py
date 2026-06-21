from django.contrib.auth.models import User
from rest_framework import status
from store.models import Collection
import pytest
from model_bakery import baker



@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/',collection)
    return do_create_collection



@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self,create_collection):
        response = create_collection({'title':'a'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self,authenticate,create_collection):
        authenticate()
        response = create_collection({'title':'a'})
        #Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self,authenticate,create_collection):
        authenticate(is_staff=True)
        response = create_collection({'title':''})
        #Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self,authenticate,create_collection):
        authenticate(is_staff=True)
        response = create_collection({'title':'a'})
        #Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self,api_client):

        collection = baker.make(Collection)
        response = api_client.get(f'/store/collections/{collection.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id':collection.id,
            'title':collection.title,
            'products_count':0
        }



@pytest.mark.django_db
class TestListCollection:
    def test_returns_collections(self,api_client):
        collection = baker.make(Collection)

        response = api_client.get('/store/collections/')

        assert response.status_code == status.HTTP_200_OK
        assert any(item['id'] == collection.id for item in response.data)


@pytest.mark.django_db
class TestUpdateCollection:
    def test_if_user_is_anonymous_returns_401(self,api_client):
        collection = baker.make(Collection)

        response = api_client.patch(f'/store/collections/{collection.id}/',{'title':'Updated'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self,authenticate,api_client):
        authenticate()
        collection = baker.make(Collection)

        response = api_client.patch(f'/store/collections/{collection.id}/',{'title':'Updated'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self,authenticate,api_client):
        authenticate(is_staff=True)
        collection = baker.make(Collection)

        response = api_client.patch(f'/store/collections/{collection.id}/',{'title':'Updated'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated'


@pytest.mark.django_db
class TestDeleteCollection:
    def test_if_user_is_anonymous_returns_401(self,api_client):
        collection = baker.make(Collection)

        response = api_client.delete(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self,authenticate,api_client):
        authenticate()
        collection = baker.make(Collection)

        response = api_client.delete(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_collection_has_products_returns_405(self,authenticate,api_client):
        authenticate(is_staff=True)
        product = baker.make('store.Product')

        response = api_client.delete(f'/store/collections/{product.collection.id}/')

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_if_collection_has_no_products_returns_204(self,authenticate,api_client):
        authenticate(is_staff=True)
        collection = baker.make(Collection)

        response = api_client.delete(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

