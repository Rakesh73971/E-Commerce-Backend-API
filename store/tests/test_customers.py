import pytest
from django.contrib.auth.models import Permission
from rest_framework import status

from store.models import Customer


@pytest.fixture
def customer(create_customer):
    return create_customer()


@pytest.mark.django_db
class TestListCustomers:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get('/store/customers/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, api_client):
        authenticate()

        response = api_client.get('/store/customers/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, authenticate, api_client, create_customer):
        authenticate(is_staff=True)
        create_customer()

        response = api_client.get('/store/customers/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


@pytest.mark.django_db
class TestRetrieveCustomer:
    def test_if_user_is_admin_returns_200(self, authenticate, api_client, create_customer):
        authenticate(is_staff=True)
        customer = create_customer()

        response = api_client.get(f'/store/customers/{customer.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == customer.id


@pytest.mark.django_db
class TestMe:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get('/store/customers/me/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_customer(self, api_client, customer):
        api_client.force_authenticate(user=customer.user)

        response = api_client.get('/store/customers/me/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == customer.id
        assert response.data['user_id'] == customer.user.id

    def test_if_data_is_valid_updates_customer(self, api_client, customer):
        api_client.force_authenticate(user=customer.user)

        response = api_client.post('/store/customers/me/', {
            'phone': '12345',
            'birth_date': '2000-01-01',
            'membership': Customer.MEMBERSHIP_GOLD,
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['phone'] == '12345'
        assert response.data['birth_date'] == '2000-01-01'
        assert response.data['membership'] == Customer.MEMBERSHIP_GOLD


@pytest.mark.django_db
class TestCustomerHistory:
    def test_if_user_does_not_have_permission_returns_403(self, api_client, customer):
        api_client.force_authenticate(user=customer.user)

        response = api_client.get(f'/store/customers/{customer.id}/history/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_has_permission_returns_200(self, api_client, customer):
        permission = Permission.objects.get(codename='view_history')
        customer.user.user_permissions.add(permission)
        api_client.force_authenticate(user=customer.user)

        response = api_client.get(f'/store/customers/{customer.id}/history/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == 'ok'
