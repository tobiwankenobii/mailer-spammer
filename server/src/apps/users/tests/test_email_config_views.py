import pytest
from django import urls

from apps.users.models import User


@pytest.mark.django_db
def test_user_register(client):
    assert User.objects.count() == 0
    signup_url = urls.reverse("user_register")
    response = client.post(
        signup_url,
        {
            "username": "user",
            "email": "user@example.com",
            "password": "userexample",
        },
    )
    assert User.objects.count() == 1
    assert response.status_code == 201


@pytest.mark.parametrize(
    "credentials",
    [
        {},
        {
            "username": "user",
            "email": "user@example",
            "password": "userexample",
        },
    ],
)
@pytest.mark.django_db
def test_user_register_wrong_credentials(client, credentials):
    assert User.objects.count() == 0
    signup_url = urls.reverse("user_register")
    response = client.post(signup_url, credentials)
    assert User.objects.count() == 0
    assert response.status_code == 400


@pytest.mark.parametrize(
    "credentials",
    [
        {
            "username": "another_user",
            "email": "user@example.com",
            "password": "userexample",
        },
        {
            "username": "user",
            "email": "another_user@example.com",
            "password": "userexample",
        },
    ],
)
@pytest.mark.django_db
def test_user_register_existing_user(client, credentials):
    User.objects.create(username="user", email="user@example.com")
    assert User.objects.count() == 1
    signup_url = urls.reverse("user_register")
    response = client.post(signup_url, credentials)
    assert User.objects.count() == 1
    assert response.status_code == 400


@pytest.mark.django_db
def test_obtain_token_view(api_client):
    token_url = urls.reverse("token_obtain_pair")
    response = api_client.post(
        token_url,
        {
            "username": "base_user",
            "password": "base_user",
        },
    )
    assert response.status_code == 200
