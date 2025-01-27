import uuid

import pytest


@pytest.fixture
def rest_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def test_password():
    return "strong-test-password"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def rest_client_with_credentials(db, create_user, rest_client):
    user = create_user()
    rest_client.force_authenticate(user=user)
    rest_client.user = user
    yield rest_client
    rest_client.logout()
