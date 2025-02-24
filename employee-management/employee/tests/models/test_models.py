from django.test import TestCase
from decimal import Decimal
from employee.models import Department, Employee, Contact, Project, ProjectAssignment


class EmployeeModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Engineering")
        self.employee = Employee.objects.create(
            first_name="John",
            last_name="Doe",
            age=30,
            status="Active",
            salary=Decimal("5000.00"),
            department=self.department,
            role="Manager",
        )

    def test_employee_full_name(self):
        """Test that the full_name property works correctly."""
        self.assertEqual(self.employee.full_name, "John Doe")

    def test_employee_str(self):
        """Test that the string representation of an employee is the full name."""
        self.assertEqual(str(self.employee), "John Doe")


class DepartmentModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="HR")

    def test_department_str(self):
        """Test that the string representation of a department is its name."""
        self.assertEqual(str(self.department), "HR")


class ContactModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="HR")
        self.employee = Employee.objects.create(
            first_name="Jane",
            last_name="Doe",
            age=28,
            status="Active",
            salary=Decimal("4000.00"),
            department=self.department,
            role="Employee",
            email="jane.doe@example.com",
        )

        self.contact = Contact.objects.create(
            employee=self.employee, value="contact@example.com", contact_type="Contact"
        )

    def test_contact_str(self):
        """Test that the string representation of a contact is 'Contact for [employee full name]'."""
        expected = f"Contact for {self.employee.full_name}"
        self.assertEqual(str(self.contact), expected)


class ProjectModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Engineering")
        self.project = Project.objects.create(
            name="Project A", description="Test Project"
        )
        self.admin = Employee.objects.create(
            first_name="Admin",
            last_name="User",
            age=35,
            status="Active",
            salary=Decimal("8000.00"),
            department=self.department,
            role="Admin",
            email="admin1@example.com",
        )
        self.manager = Employee.objects.create(
            first_name="Manager",
            last_name="User",
            age=40,
            status="Active",
            salary=Decimal("7000.00"),
            department=self.department,
            role="Manager",
            email="admin@2example.com",
        )

    def test_project_str(self):
        """Test that the string representation of a project is its name."""
        self.assertEqual(str(self.project), "Project A")


class SignalTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Engineering")
        self.admin = Employee.objects.create(
            first_name="Admin",
            last_name="User",
            age=35,
            status="Active",
            salary=Decimal("8000.00"),
            department=self.department,
            role="Admin",
            email="admin2@example.com",
        )
        self.manager = Employee.objects.create(
            first_name="Manager",
            last_name="User",
            age=40,
            status="Active",
            salary=Decimal("7000.00"),
            department=self.department,
            role="Manager",
            email="manager2@example.com",
        )
        # Creating a new project should trigger the signal.
        self.project = Project.objects.create(
            name="Project C", description="Test Project C"
        )

    def test_signal_auto_add_high_role_members(self):
        """Test that the signal correctly adds Admin and Manager employees to the project."""
        assignments = ProjectAssignment.objects.filter(project=self.project)
        assigned_emails = {assignment.employee.email for assignment in assignments}
        self.assertIn(self.admin.email, assigned_emails)
        self.assertIn(self.manager.email, assigned_emails)
