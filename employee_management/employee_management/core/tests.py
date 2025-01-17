from decimal import Decimal
from django.test import TestCase
from .models import Department, Contact, Employee, Project, ProjectAssignment


class EmployeeModelTest(TestCase):
    def setUp(self):
        # Setup test data
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

    def test_employee_age_over_25(self):
        """Test the custom manager 'aged_over_25'."""
        employee2 = Employee.objects.create(
            first_name="Jane",
            last_name="Doe",
            age=24,
            status="Active",
            salary=Decimal("4000.00"),
            department=self.department,
            role="Employee",
        )

        employees = Employee.objects.aged_over_25()
        self.assertIn(self.employee, employees)
        self.assertNotIn(employee2, employees)


class ProjectModelTest(TestCase):
    def setUp(self):
        # Setup test data
        self.department = Department.objects.create(name="Engineering")
        self.project = Project.objects.create(
            name="Project A", description="Test Project"
        )

    def test_project_str(self):
        """Test that the string representation of a project is its name."""
        self.assertEqual(str(self.project), "Project A")

    def test_project_assignment(self):
        """Test that a project can have multiple employees assigned."""
        employee = Employee.objects.create(
            first_name="Alice",
            last_name="Smith",
            age=30,
            status="Active",
            salary=Decimal("6000.00"),
            department=self.department,
            role="Admin",
        )

        ProjectAssignment.objects.create(
            employee=employee, project=self.project, role="Admin"
        )

        assignment = ProjectAssignment.objects.get(
            employee=employee, project=self.project
        )
        self.assertEqual(assignment.role, "Admin")
        self.assertEqual(assignment.project.name, "Project A")
        self.assertEqual(assignment.employee.full_name, "Alice Smith")


class SignalTest(TestCase):
    def setUp(self):
        # Setup test data for signal
        self.department = Department.objects.create(name="Engineering")
        self.project = Project.objects.create(
            name="Project B", description="Test Project B"
        )

        # Add employees with different roles
        self.admin = Employee.objects.create(
            first_name="Admin",
            last_name="User",
            age=35,
            status="Active",
            salary=Decimal("8000.00"),
            department=self.department,
            role="Admin",
        )
        self.manager = Employee.objects.create(
            first_name="Manager",
            last_name="User",
            age=40,
            status="Active",
            salary=Decimal("7000.00"),
            department=self.department,
            role="Manager",
        )
        self.employee = Employee.objects.create(
            first_name="Employee",
            last_name="User",
            age=25,
            status="Active",
            salary=Decimal("5000.00"),
            department=self.department,
            role="Employee",
        )

    def test_signal_auto_add_high_role_members(self):
        """Test that employees with the highest role are automatically added to a project."""
        # Create a project and check if high role employees are added
        self.project = Project.objects.create(
            name="Project C", description="Test Project C"
        )

        # Check the assignments
        assignments = ProjectAssignment.objects.filter(project=self.project)

        # Admin and Manager should be added, but not Employee (assuming Admin is the highest role)
        self.assertEqual(
            assignments.count(), 2
        )  # Only Admin and Manager should be added
        self.assertTrue(assignments.filter(employee=self.admin).exists())
        self.assertTrue(assignments.filter(employee=self.manager).exists())
        self.assertFalse(assignments.filter(employee=self.employee).exists())


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
            role="Manager",
        )
        self.contact = Contact.objects.create(
            employee=self.employee, address="1234 Elm Street"
        )

    def test_contact_str(self):
        """Test that the string representation of a contact is 'Contact for [employee]'."""
        self.assertEqual(str(self.contact), f"Contact for {self.employee.full_name}")
