import typing as T  # noqa:N812

import pytest
from django.db.models import Model
from django.utils import timezone

from apps.emails.models import EmailConfig
from apps.users.models import User


def generate_configs(amount: int):
    """Generates x number of EmailConfig instances."""
    author = User.objects.get(username="base_user")
    configs = [
        EmailConfig(
            **{
                "author": author,
                "recipient": "recipient@test.com",
                "subject": "Test",
                "content": "Content",
            }
        )
        for _ in range(amount)
    ]
    EmailConfig.objects.bulk_create(configs)


def check_every_field_for_instance(instance: Model, data: T.Dict):
    """Checks for every field in given instance, comparing to given config."""
    instance.refresh_from_db()
    for field in data.keys():
        assert getattr(instance, field) == data[field]


@pytest.mark.django_db
def test_email_config_crud_unauthorized(client):
    response = client.get("/api/email-configs/")
    assert response.status_code == 401
    response = client.post("/api/email-configs/", {})
    assert response.status_code == 401
    response = client.patch("/api/email-configs/1/", {})
    assert response.status_code == 401
    response = client.delete("/api/email-configs/1/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_email_config_retrieve(api_client):
    generate_configs(3)
    assert EmailConfig.objects.count() == 3
    list_response = api_client.get("/api/email-configs/")
    assert list_response.status_code == 200
    assert len(list_response.data) == 3

    random_config = EmailConfig.objects.first()
    get_response = api_client.get(f"/api/email-configs/{random_config.pk}/")
    assert get_response.status_code == 200
    check_every_field_for_instance(random_config, get_response.data)


@pytest.mark.django_db
def test_email_config_create(api_client):
    assert EmailConfig.objects.count() == 0
    data = {
        "recipient": "recipient@test.com",
        "subject": "Test",
        "content": "Content",
        "send_at": timezone.now(),
    }
    response = api_client.post("/api/email-configs/", data)
    config = EmailConfig.objects.first()
    assert response.status_code == 201
    check_every_field_for_instance(config, data)


@pytest.mark.django_db
def test_email_config_create_with_wrong_author(api_client):
    author = User.objects.create(username="wrong_user", email="wrong@user.com")
    assert EmailConfig.objects.count() == 0
    response = api_client.post(
        "/api/email-configs/",
        {
            "author": author.pk,
            "recipient": "recipient@test.com",
            "subject": "Test",
            "content": "Content",
            "send_at": timezone.now(),
        },
    )
    assert response.status_code == 201
    assert EmailConfig.objects.get(pk=response.data["pk"]).author != author


@pytest.mark.django_db
def test_email_config_update(api_client):
    generate_configs(1)
    config = EmailConfig.objects.first()
    new_data = {
        "recipient": "new@test.com",
        "subject": "New Subject",
        "content": "New Content",
        "send_at": timezone.now(),
    }
    response = api_client.patch(
        f"/api/email-configs/{config.pk}/",
        new_data,
    )
    assert response.status_code == 200
    check_every_field_for_instance(config, new_data)


@pytest.mark.django_db
def test_email_config_update_wrong_author(api_client):
    generate_configs(1)
    author = User.objects.create(username="wrong_user", email="wrong@user.com")
    config = EmailConfig.objects.first()
    new_data = {
        "author": author.pk,
        "recipient": "new@test.com",
        "subject": "New Subject",
        "content": "New Content",
        "send_at": timezone.now(),
    }
    response = api_client.patch(
        f"/api/email-configs/{config.pk}/",
        new_data,
    )
    assert response.status_code == 200
    assert EmailConfig.objects.get(pk=response.data["pk"]).author != author


@pytest.mark.django_db
def test_email_config_delete(api_client):
    generate_configs(1)
    config = EmailConfig.objects.first()
    response = api_client.delete(
        f"/api/email-configs/{config.pk}/",
    )
    assert response.status_code == 204
    assert EmailConfig.objects.count() == 0


@pytest.mark.django_db
def test_email_config_permissions(api_client):
    generate_configs(1)
    new_author = User.objects.create(
        username="wrong_user", email="wrong@user.com"
    )
    config = EmailConfig.objects.first()
    config.author = new_author
    config.save()

    response = api_client.get("/api/email-configs/")
    assert response.status_code == 200
    assert len(response.data) == 0
    response = api_client.patch(f"/api/email-configs/{config.pk}/", {})
    assert response.status_code == 404
    response = api_client.delete(f"/api/email-configs/{config.pk}/")
    assert response.status_code == 404
