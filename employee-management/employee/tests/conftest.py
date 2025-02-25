# tests/conftest.py
from django.conf import settings
import pytest
from rest_framework.test import APIClient
from employee.models import Employee, Department, Project


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def department(db):
    return Department.objects.create(
        name="IT Department", description="Handles tech-related tasks.", code="IT01"
    )


@pytest.fixture
def admin_user(db, department):
    # Create an admin user
    return Employee.objects.create_superuser(
        email="admin@example.com",
        password="password123",
        first_name="Admin",
        last_name="User",
        age=30,
        status="Active",
        department=department,
        role="admin",
    )


@pytest.fixture
def manager_user(db, department):
    return Employee.objects.create_user(
        email="manager@example.com",
        password="password123",
        first_name="Manager",
        last_name="User",
        age=35,
        status="Active",
        department=department,
        role="manager",
    )


@pytest.fixture
def employee_user(db, department):
    return Employee.objects.create_user(
        email="employee@example.com",
        password="password123",
        first_name="Employee",
        last_name="User",
        age=28,
        status="Active",
        department=department,
        role="employee",
    )


@pytest.fixture
def sample_employee(db, department):
    return Employee.objects.create_user(
        email="sample@example.com",
        password="password123",
        first_name="Sample",
        last_name="Employee",
        age=30,
        status="Active",
        department=department,
        role="employee",
    )


@pytest.fixture
def create_employees(db, department):
    employees = []
    for name in ["Alice", "Bob", "Charlie", "David"]:
        emp = Employee.objects.create_user(
            email=f"{name.lower()}@example.com",
            password="password123",
            first_name=name,
            last_name="Test",
            age=25,
            status="Active",
            department=department,
            role="employee",
        )
        employees.append(emp)
    return employees


@pytest.fixture
def create_many_employees(db, department):
    employees = []
    for i in range(25):  # Create 15 employees to test pagination
        emp = Employee.objects.create_user(
            email=f"emp{i}@example.com",
            password="password123",
            first_name=f"Emp{i}",
            last_name="Test",
            age=25,
            status="Active",
            department=department,
            role="employee",
        )
        employees.append(emp)
    return employees


@pytest.fixture
def sample_project(db):
    return Project.objects.create(
        name="Sample Project", description="A sample project for testing."
    )
