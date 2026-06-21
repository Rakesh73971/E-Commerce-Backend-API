import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from store.models import Customer


@pytest.fixture
def api_client():
    return APIClient()
    
@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate

@pytest.fixture
def create_user():
    def do_create_user(**kwargs):
        user_count = get_user_model().objects.count()
        return get_user_model().objects.create_user(
            username=kwargs.pop('username', f'user-{user_count + 1}'),
            email=kwargs.pop('email', f'user-{user_count + 1}@example.com'),
            password=kwargs.pop('password', 'password'),
            **kwargs
        )
    return do_create_user

@pytest.fixture
def create_customer(create_user):
    def do_create_customer(**kwargs):
        user = kwargs.pop('user', None) or create_user()
        customer = Customer.objects.get(user=user)
        for key, value in kwargs.items():
            setattr(customer, key, value)
        customer.save()
        return customer
    return do_create_customer
