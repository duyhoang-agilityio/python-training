import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_create_department(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    payload = {
        "name": "HR Department",
        "description": "Handles human resources.",
        "code": "HR01",
    }
    url = reverse("department-list")
    response = api_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == payload["name"]


@pytest.mark.django_db
def test_update_employee(api_client, admin_user, sample_employee):
    api_client.force_authenticate(user=admin_user)
    payload = {"first_name": "UpdatedName"}
    url = reverse("employee-detail", args=[sample_employee.id])
    response = api_client.patch(url, payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == "UpdatedName"


@pytest.mark.django_db
def test_create_contact(api_client, admin_user, sample_employee):
    api_client.force_authenticate(user=admin_user)
    payload = {
        "employee": sample_employee.id,
        "contact_type": "email",
        "value": "contact@example.com",
    }
    url = reverse("contact-list")
    response = api_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["value"] == "contact@example.com"


@pytest.mark.django_db
def test_delete_project(api_client, admin_user, sample_project):
    api_client.force_authenticate(user=admin_user)
    url = reverse("project-detail", args=[sample_project.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
