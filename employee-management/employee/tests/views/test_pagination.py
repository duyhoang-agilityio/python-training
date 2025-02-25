import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestEmployeePagination:
    def test_employee_pagination(self, api_client, admin_user, create_many_employees):
        """
        Test that the employee list endpoint correctly paginates results.
        Assumes a default page size of 10.
        """
        api_client.force_authenticate(user=admin_user)
        url = reverse("employee-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        
        # Check that pagination keys are present.
        assert "results" in response.data
        assert "next" in response.data
        assert "previous" in response.data
        
        # Check that the page size does not exceed 10.
        assert len(response.data["results"]) <= 10
