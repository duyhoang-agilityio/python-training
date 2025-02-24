import pytest
from django.urls import reverse
from rest_framework import status
from employee.models import Employee, Department, Project


@pytest.mark.django_db
def test_ordering_employees(api_client, admin_user, create_employees):
    api_client.force_authenticate(user=admin_user)
    url = reverse("employee-list") + "?ordering=first_name"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    names = [emp["first_name"] for emp in response.data["results"]]
    assert names == sorted(names)


@pytest.mark.django_db
def test_search_employee(api_client, admin_user, create_employees):
    api_client.force_authenticate(user=admin_user)
    url = reverse("employee-list") + "?search=Alice"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    results = response.data["results"]
    # Ensure that at least one result contains "Alice" in first_name or last_name.
    assert any(
        "Alice" in emp["first_name"] or "Alice" in emp["last_name"] for emp in results
    )
