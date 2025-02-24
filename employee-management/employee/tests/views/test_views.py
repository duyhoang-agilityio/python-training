import pytest
from django.urls import reverse
from rest_framework import status
from employee.models import Department, Employee, Contact, Project


@pytest.mark.django_db
class TestEmployeeViewSet:
    def test_unauthenticated_access(self, api_client):
        url = reverse("employee-list")
        response = api_client.get(url)
        # With DRF's IsAuthenticatedOrReadOnly default, expect 403 Forbiden
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_employees_as_admin(self, api_client, admin_user):
        # Create some sample employees
        department = Department.objects.create(name="Test Department")
        Employee.objects.create(
            first_name="User1",
            last_name="Test",
            age=30,
            status="Active",
            salary="5000.00",
            department=department,
            role="Employee",
            email="user1@example.com",
        )
        Employee.objects.create(
            first_name="User2",
            last_name="Test",
            age=35,
            status="Active",
            salary="6000.00",
            department=department,
            role="Employee",
            email="user2@example.com",
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse("employee-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # Expect a paginated list containing our employees.
        assert "results" in response.data
        assert len(response.data["results"]) >= 2

    def test_retrieve_employee_detail(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        department = Department.objects.create(name="Test Dept")
        employee = Employee.objects.create(
            first_name="Detail",
            last_name="User",
            age=32,
            status="Active",
            salary="5500.00",
            department=department,
            role="Employee",
            email="detail@example.com",
        )
        url = reverse("employee-detail", args=[employee.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == "detail@example.com"


@pytest.mark.django_db
class TestContactViewSet:
    def test_list_contacts(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        department = Department.objects.create(name="HR")
        employee = Employee.objects.create(
            first_name="Contact",
            last_name="User",
            age=28,
            status="Active",
            salary="4000.00",
            department=department,
            role="Employee",
            email="contactuser@example.com",
        )
        # Create a contact for this employee
        Contact.objects.create(
            employee=employee, contact_type="email", value="contact@example.com"
        )
        url = reverse("contact-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        # Check that at least one contact is returned
        assert len(response.data["results"]) >= 1


@pytest.mark.django_db
class TestDepartmentViewSet:
    def test_list_departments(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        Department.objects.create(name="Dept A")
        Department.objects.create(name="Dept B")
        url = reverse("department-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) >= 2

    def test_add_employees_action(self, api_client, admin_user, sample_employee):
        # This test uses the custom action 'add-employees' on the Department view.
        api_client.force_authenticate(user=admin_user)
        department = Department.objects.create(name="Sales")
        url = reverse("department-add-employees", args=[department.id])
        payload = {"employee_ids": [sample_employee.id]}
        response = api_client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        sample_employee.refresh_from_db()
        assert sample_employee.department == department


@pytest.mark.django_db
class TestProjectViewSet:
    def test_list_projects(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        Project.objects.create(name="Proj 1", description="Test project 1")
        Project.objects.create(name="Proj 2", description="Test project 2")
        url = reverse("project-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) >= 2

    def test_assign_employees_action(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        department = Department.objects.create(name="IT")
        project = Project.objects.create(
            name="Proj Assign", description="Assignment test"
        )
        employee = Employee.objects.create(
            first_name="Assign",
            last_name="User",
            age=30,
            status="Active",
            salary="5000.00",
            department=department,
            role="Employee",
            email="assignuser@example.com",
        )
        url = reverse("project-assign-employees", args=[project.id])
        payload = {"assignments": [{"employee": employee.id, "role": "Developer"}]}
        response = api_client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        project.refresh_from_db()
        # Check that an assignment has been created for the employee
        assert project.projectassignment_set.count() == 2
