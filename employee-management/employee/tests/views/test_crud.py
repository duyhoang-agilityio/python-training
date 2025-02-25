from employee.models import Department, Contact, Employee, Project
from .base_CRUD_test import BaseCRUDTest


class DepartmentCRUDTest(BaseCRUDTest):
    model = Department
    url_basename = "department"
    create_data = {
        "name": "HR Department",
        "description": "Handles human resources.",
        "code": "HR01",
    }
    update_data = {"name": "Updated HR Department"}

    def setUp(self):
        super().setUp()
        # Create an admin user for authentication.
        admin_dept = Department.objects.create(
            name="Admin Department", description="Admin Dept", code="ADM"
        )
        self.admin_user = Employee.objects.create_superuser(
            email="admin@example.com",
            password="password123",
            first_name="Admin",
            last_name="User",
            age=30,
            status="Active",
            department=admin_dept,
            role="admin",
        )
        self.client.force_authenticate(user=self.admin_user)


class ContactCRUDTest(BaseCRUDTest):
    model = Contact
    url_basename = "contact"

    def setUp(self):
        super().setUp()
        # Create an admin user for authentication.
        admin_dept = Department.objects.create(
            name="Admin Dept", description="Admin Dept", code="ADM"
        )
        self.admin_user = Employee.objects.create_superuser(
            email="admin_contact@example.com",
            password="password123",
            first_name="Admin",
            last_name="User",
            age=30,
            status="Active",
            department=admin_dept,
            role="admin",
        )
        self.client.force_authenticate(user=self.admin_user)
        # Create a related employee for the contact.
        self.contact_employee = Employee.objects.create_user(
            email="contactuser@example.com",
            password="password123",
            first_name="Contact",
            last_name="User",
            age=28,
            status="Active",
            department=admin_dept,
            role="employee",
        )

    @property
    def create_data(self):
        # Pass the employee instance (not just the ID) when creating a model instance.
        return {
            "employee": self.contact_employee,
            "contact_type": "email",
            "value": "contact@example.com",
        }

    @property
    def update_data(self):
        return {"value": "updated_contact@example.com"}


class ProjectCRUDTest(BaseCRUDTest):
    model = Project
    url_basename = "project"
    create_data = {"name": "Test Project", "description": "This is a test project."}
    update_data = {
        "name": "Updated Test Project",
        "description": "This is an updated description.",
    }

    def setUp(self):
        super().setUp()
        # Create an admin user for authentication.
        admin_dept = Department.objects.create(
            name="Admin Dept", description="Admin Dept", code="ADM"
        )
        self.admin_user = Employee.objects.create_superuser(
            email="admin_project@example.com",
            password="password123",
            first_name="Admin",
            last_name="User",
            age=30,
            status="Active",
            department=admin_dept,
            role="admin",
        )
        self.client.force_authenticate(user=self.admin_user)
