import pytest
from decimal import Decimal
from employee.models import Department, Employee, Contact, Project, ProjectAssignment
from employee.serializers import (
    ContactSerializer,
    EmployeeSerializer,
    DepartmentSerializer,
    ProjectAssignmentSerializer,
    ProjectSerializer,
)

@pytest.mark.django_db
class TestContactSerializer:
    def test_serialization(self, create_employees):
        # Use the create_employees fixture; pick an employee (e.g. Alice)
        employee = next(emp for emp in create_employees if emp.first_name == "Alice")
        contact = Contact.objects.create(
            employee=employee, contact_type="email", value="alice@example.com"
        )
        serializer = ContactSerializer(contact)
        data = serializer.data
        assert data["id"] == contact.id
        assert data["employee"] == employee.id
        assert data["contact_type"] == "email"
        assert data["value"] == "alice@example.com"

    def test_str_method_default(self, create_employees):
        # Use the create_employees fixture; pick an employee (e.g. Bob)
        employee = next(emp for emp in create_employees if emp.first_name == "Bob")
        contact = Contact.objects.create(
            employee=employee, contact_type="Contact", value="bob@example.com"
        )
        expected = f"Contact for {employee.first_name} {employee.last_name}"
        assert str(contact) == expected


@pytest.mark.django_db
class TestEmployeeSerializer:
    def test_serialization(self, department):
        employee = Employee.objects.create(
            first_name="Carol",
            last_name="White",
            age=40,
            status="Active",
            salary=Decimal("7000.00"),
            department=department,
            role="Manager",
            email="carol.white@example.com",
        )
        serializer = EmployeeSerializer(employee)
        data = serializer.data
        assert data["id"] == employee.id
        assert data["first_name"] == "Carol"
        assert data["last_name"] == "White"
        assert data["full_name"] == "Carol White"
        assert data["contacts"] == []

    def test_validate_salary(self):
        data = {
            "first_name": "Dave",
            "last_name": "Brown",
            "age": 30,
            "email": "dave.brown@example.com",
            "status": "Active",
            "salary": -1000,
            "department": None,
            "role": "Employee",
        }
        serializer = EmployeeSerializer(data=data)
        assert not serializer.is_valid()
        assert "salary" in serializer.errors
        assert "Salary cannot be negative." in serializer.errors["salary"][0]

    def test_validate_age(self):
        data = {
            "first_name": "Eve",
            "last_name": "Black",
            "age": 15,
            "email": "eve.black@example.com",
            "status": "Active",
            "salary": 3000,
            "department": None,
            "role": "Employee",
        }
        serializer = EmployeeSerializer(data=data)
        assert not serializer.is_valid()
        assert "age" in serializer.errors

        data["age"] = 101
        serializer = EmployeeSerializer(data=data)
        assert not serializer.is_valid()
        assert "age" in serializer.errors


@pytest.mark.django_db
class TestDepartmentSerializer:
    def test_employee_count(self, department):
        # department fixture from conftest is used here.
        serializer = DepartmentSerializer(department)
        data = serializer.data
        assert data["employee_count"] == 0

        Employee.objects.create(
            first_name="Frank",
            last_name="Green",
            age=50,
            status="Active",
            salary=Decimal("8000.00"),
            department=department,
            role="Manager",
            email="frank.green@example.com",
        )
        Employee.objects.create(
            first_name="Grace",
            last_name="Hill",
            age=45,
            status="Active",
            salary=Decimal("7500.00"),
            department=department,
            role="Employee",
            email="grace.hill@example.com",
        )
        serializer = DepartmentSerializer(department)
        data = serializer.data
        assert data["employee_count"] == 2
        assert len(data["employees"]) == 2


@pytest.mark.django_db
class TestProjectAssignmentSerializer:
    def test_validate_duplicate_assignment(self, department):
        employee = Employee.objects.create(
            first_name="Henry",
            last_name="Ivy",
            age=30,
            status="Active",
            salary=Decimal("5500.00"),
            department=department,
            role="Employee",
            email="henry.ivy@example.com",
        )
        project = Project.objects.create(name="Project X", description="Secret Project")
        ProjectAssignment.objects.create(
            employee=employee, project=project, role="Developer"
        )
        data = {"employee_id": employee.id, "role": "Developer"}
        serializer = ProjectAssignmentSerializer(data=data, context={"project": project})
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors
        assert "already assigned" in serializer.errors["non_field_errors"][0]


@pytest.mark.django_db
class TestProjectSerializer:
    def test_validate_employee_assignments_missing_keys(self):
        # Missing 'role' key.
        data = {
            "name": "Project Z",
            "description": "Invalid assignments",
            "employee_assignments": [{"employee": 1}],
        }
        serializer = ProjectSerializer(data=data)
        assert not serializer.is_valid()
        error_message = serializer.errors["employee_assignments"][0]
        assert "missing 'role' key" in error_message

        # Missing 'employee' key.
        data = {
            "name": "Project Z",
            "description": "Invalid assignments",
            "employee_assignments": [{"role": "Developer"}],
        }
        serializer = ProjectSerializer(data=data)
        assert not serializer.is_valid()
        error_message = serializer.errors["employee_assignments"][0]
        assert "missing 'employee' key" in error_message

    def test_create_project_with_assignments(self, department):
        emp1 = Employee.objects.create(
            first_name="Jack",
            last_name="King",
            age=29,
            status="Active",
            salary=Decimal("4500.00"),
            department=department,
            role="Employee",
            email="jack.king@example.com",
        )
        emp2 = Employee.objects.create(
            first_name="Liam",
            last_name="Moore",
            age=35,
            status="Active",
            salary=Decimal("5000.00"),
            department=department,
            role="Employee",
            email="liam.moore@example.com",
        )
        data = {
            "name": "Project New",
            "description": "Testing creation with assignments",
            "employee_assignments": [
                {"employee": emp1.id, "role": "Developer"},
                {"employee": emp2.id, "role": "Tester"},
            ],
        }
        serializer = ProjectSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        project = serializer.save()
        assert project.name == "Project New"
        assignments = project.projectassignment_set.all()
        assert assignments.count() == 2
        roles = {a.role for a in assignments}
        assert "Developer" in roles
        assert "Tester" in roles

    def test_update_project_assignments(self, department):
        emp1 = Employee.objects.create(
            first_name="Nina",
            last_name="Olsen",
            age=30,
            status="Active",
            salary=Decimal("4800.00"),
            department=department,
            role="Employee",
            email="nina.olsen@example.com",
        )
        project = Project.objects.create(name="Project Update", description="Initial Description")
        ProjectAssignment.objects.create(
            employee=emp1, project=project, role="Designer"
        )
        emp2 = Employee.objects.create(
            first_name="Oscar",
            last_name="Perry",
            age=32,
            status="Active",
            salary=Decimal("5200.00"),
            department=department,
            role="Employee",
            email="oscar.perry@example.com",
        )
        data = {
            "name": "Project Update",
            "description": "Updated Description",
            "employee_assignments": [{"employee": emp2.id, "role": "Lead Designer"}],
        }
        serializer = ProjectSerializer(instance=project, data=data)
        assert serializer.is_valid(), serializer.errors
        updated_project = serializer.save()
        assert updated_project.description == "Updated Description"
        assignments = updated_project.projectassignment_set.all()
        assert assignments.count() == 1
        assignment = assignments.first()
        assert assignment.employee == emp2
        assert assignment.role == "Lead Designer"

    def test_create_project_no_assignments(self):
        data = {
            "name": "Project Without Assignments",
            "description": "Testing creation with no assignments",
        }
        serializer = ProjectSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        project = serializer.save()
        assert project.name == "Project Without Assignments"
        assert project.projectassignment_set.count() == 0

    def test_update_project_clear_assignments(self, department):
        emp1 = Employee.objects.create(
            first_name="Peter",
            last_name="Quinn",
            age=34,
            status="Active",
            salary=Decimal("5100.00"),
            department=department,
            role="Employee",
            email="peter.quinn@example.com",
        )
        project = Project.objects.create(name="Project Clear", description="Will remove assignments")
        ProjectAssignment.objects.create(
            employee=emp1, project=project, role="Designer"
        )
        data = {
            "name": "Project Clear",
            "description": "All assignments removed",
            "employee_assignments": [],
        }
        serializer = ProjectSerializer(instance=project, data=data)
        assert serializer.is_valid(), serializer.errors
        updated_project = serializer.save()
        # Should remove existing assignments.
        assert updated_project.projectassignment_set.count() == 0
