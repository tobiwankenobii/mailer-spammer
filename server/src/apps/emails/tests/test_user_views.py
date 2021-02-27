import pytest
from django.utils import timezone

from apps.emails.models import EmailConfig
from apps.users.models import User


def generate_configs(amount: int):
    author = User.objects.get(username="base_user")
    configs = [
        EmailConfig(
            **{
                "author": author,
                "recipient": "recipient@test.com",
                "subject": "Test",
                "content": "Content",
                "send_at": timezone.now(),
            }
        )
        for _ in range(amount)
    ]
    EmailConfig.objects.bulk_create(configs)


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
    assert get_response.data["pk"] == random_config.pk


@pytest.mark.django_db
def test_email_config_create(api_client):
    assert EmailConfig.objects.count() == 0
    response = api_client.post(
        "/api/email-configs/",
        {
            "recipient": "recipient@test.com",
            "subject": "Test",
            "content": "Content",
            "send_at": timezone.now(),
        },
    )
    assert response.status_code == 201


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
    assert EmailConfig.objects.get(pk=response.data['pk']).author != author
