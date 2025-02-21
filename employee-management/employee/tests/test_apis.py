from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from employee.models import Employee, Department, Contact, Project, ProjectAssignment


User = get_user_model()


class BaseAPITest(APITestCase):
    def setUp(self):
        # Create a manager (admin) user using your custom manager
        self.manager = User.objects.create_user(
            email="manager@example.com",
            first_name="Manager",
            last_name="User",
            password="managerpass",
            role="manager",
        )

        self.manager.is_staff = True
        self.manager.save()

        # Create a regular employee user
        self.employee = User.objects.create_user(
            email="employee@example.com",
            first_name="Employee",
            last_name="User",
            password="employeepass",
            role="employee",
        )
        self.employee.is_staff = False
        self.employee.save()

        # Create Departments
        self.department = Department.objects.create(
            name="IT Department", description="Information Technology", code="IT-001"
        )

        # Create API clients and authenticate
        self.manager_client = APIClient()
        self.manager_client.login(email="manager@example.com", password="managerpass")

        self.employee_client = APIClient()
        self.employee_client.login(
            email="employee@example.com", password="employeepass"
        )

        # Create some sample employees for testing listing/filtering
        self.other_employees = []
        for i in range(5):
            user = User.objects.create_user(
                email=f"employee{i}@example.com",
                first_name=f"Test{i}",
                last_name="User",
                password="password123",
                role="employee",
            )
            user.is_staff = False
            user.save()
            self.other_employees.append(user)

    def tearDown(self):
        self.client.logout()
        self.manager_client.logout()
        self.employee_client.logout()


class AuthenticationPermissionTests(BaseAPITest):
    def test_unauthenticated_access(self):
        # Unauthenticated client
        pass

    def test_manager_permission(self):

        pass

    def test_employee_permission(self):

        pass


class CRUDTests(BaseAPITest):
    def test_employee_crud(self):
        # Manager creates an employee
        pass

    def test_department_crud(self):
        pass


class ValidationTests(BaseAPITest):
    def test_invalid_email(self):
        pass

    def test_missing_required_fields(self):
        pass


class FilteringSearchingOrderingTests(BaseAPITest):
    def setUp(self):
        super().setUp()
        # Create additional employees with distinct names and birth_dates
        for i in range(3):
            User.objects.create_user(
                email=f"filter{i}@example.com",
                first_name=f"Alpha{i}",
                last_name="Test",
                password="password123",
                role="employee",
            )

    def test_ordering(self):
        pass

    def test_searching(self):
        pass

    def test_birthdate_filter(self):
        pass


class PaginationTests(BaseAPITest):
    def test_pagination(self):
        pass
