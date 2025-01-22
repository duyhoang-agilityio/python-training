from django.test import TestCase
from decimal import Decimal
from ..models import Department, Employee, Contact, Project, ProjectAssignment


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

    def test_employee_age_over_25(self):
        """Test the custom manager 'aged_over_25'."""
        employee2 = Employee.objects.create(
            first_name="Jane",
            last_name="Smith",
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

    def test_project_str(self):
        """Test that the string representation of a project is its name."""
        self.assertEqual(str(self.project), "Project A")

    def test_project_assignment_signal(self):
        """Test that employees with the highest role are added to a new project."""
        new_project = Project.objects.create(
            name="Project B", description="Test Project B"
        )

        # Check that only the Admin is added
        assignments = ProjectAssignment.objects.filter(project=new_project)
        self.assertEqual(assignments.count(), 1)
        self.assertTrue(assignments.filter(employee=self.admin).exists())
        self.assertFalse(assignments.filter(employee=self.manager).exists())


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
        )
        self.contact = Contact.objects.create(
            employee=self.employee, address="1234 Elm Street"
        )

    def test_contact_str(self):
        """Test that the string representation of a contact is 'Contact for [employee]'."""
        self.assertEqual(str(self.contact), f"Contact for {self.employee.full_name}")


class DepartmentModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="HR")

    def test_department_str(self):
        """Test that the string representation of a department is its name."""
        self.assertEqual(str(self.department), "HR")


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
            # role="Admin",
        )
        self.manager = Employee.objects.create(
            first_name="Manager",
            last_name="User",
            age=40,
            status="Active",
            salary=Decimal("7000.00"),
            department=self.department,
            # role="Manager",
        )
        self.project = Project.objects.create(
            name="Project C", description="Test Project C"
        )

    def test_signal_auto_add_high_role_members(self):
        """Test that the signal correctly adds Admin employees to the project."""
