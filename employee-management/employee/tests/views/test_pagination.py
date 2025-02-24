import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_pagination(api_client, admin_user, create_many_employees):
    api_client.force_authenticate(user=admin_user)
    url = reverse("employee-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    # Ensure pagination keys are present.
    assert "results" in response.data
    assert "next" in response.data
    assert "previous" in response.data
    # Assuming a default page size of 10.
    assert len(response.data["results"]) <= 10
