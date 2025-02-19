from rest_framework import serializers
from .models import Department, Contact, Employee, Project, ProjectAssignment


# ---------- Contact Serializer ----------
class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact model.

    Handles the serialization of contact information including contact type and value.
    """

    class Meta:
        model = Contact
        fields = ["id", "employee", "contact_type", "value"]


# ---------- Employee Serializer ----------
class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee model.

    Handles the serialization of employee information including personal details,
    department association, and related contacts.
    """

    full_name: serializers.CharField = serializers.CharField(read_only=True)
    contacts: ContactSerializer = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "age",
            "email",
            "birth_date",
            "status",
            "salary",
            "department",
            "role",
            "contacts",
        ]

    def validate_salary(self, value: float) -> float:
        """Validate that salary is positive."""
        if value < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return value

    def validate_age(self, value: int) -> int:
        """Validate that age is reasonable."""
        if value < 16 or value > 100:
            raise serializers.ValidationError("Age must be between 16 and 100.")
        return value


# ---------- Department Serializer ----------
class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model.

    Handles the serialization of department information including its employees
    and provides a computed field for employee count.
    """

    employees: EmployeeSerializer = EmployeeSerializer(many=True, read_only=True)
    employee_count: serializers.SerializerMethodField = (
        serializers.SerializerMethodField()
    )

    class Meta:
        model = Department
        fields = ["id", "name", "description", "code", "employees", "employee_count"]

    def get_employee_count(self, obj: Department) -> int:
        return obj.employees.count()


# ---------- ProjectAssignment Serializer ----------
class ProjectAssignmentSerializer(serializers.ModelSerializer):
    """Serializer for ProjectAssignment model.

    Handles the serialization of project assignments, including employee details
    and their role in the project.
    """

    employee: EmployeeSerializer = EmployeeSerializer(read_only=True)
    employee_id: serializers.PrimaryKeyRelatedField = (
        serializers.PrimaryKeyRelatedField(
            queryset=Employee.objects.all(), source="employee", write_only=True
        )
    )

    class Meta:
        model = ProjectAssignment
        fields = ["id", "employee", "employee_id", "role"]

    def validate(self, data: dict) -> dict:
        """Validate that an employee isn't assigned to the same project multiple times."""
        employee = data.get("employee")
        if ProjectAssignment.objects.filter(
            project=self.context.get("project"), employee=employee
        ).exists():
            raise serializers.ValidationError(
                "This employee is already assigned to this project."
            )
        return data


# ---------- Project Serializer ----------
class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model.

    Handles the serialization of project information including project assignments
    and provides methods for managing employee assignments.
    """

    assignments: ProjectAssignmentSerializer = ProjectAssignmentSerializer(
        source="projectassignment_set", many=True, read_only=True
    )
    employee_assignments: serializers.ListField = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
        write_only=True,
        required=False,
        help_text="List of assignments, e.g. [{'employee': 1, 'role': 'Developer'}, ...]",
    )

    class Meta:
        model = Project
        fields = ["id", "name", "description", "assignments", "employee_assignments"]

    def validate_employee_assignments(self, value: list) -> list:
        # Ensure each assignment has both 'employee' and 'role' keys.
        for idx, assignment in enumerate(value):
            if "employee" not in assignment:
                raise serializers.ValidationError(
                    f"Assignment at index {idx} is missing 'employee' key."
                )
            if "role" not in assignment:
                raise serializers.ValidationError(
                    f"Assignment at index {idx} is missing 'role' key."
                )
        return value

    def _handle_assignments(self, project: Project, assignments_data: list) -> None:
        for assignment in assignments_data:
            employee_id = assignment.get("employee")
            role = assignment.get("role", "")
            if employee_id:
                ProjectAssignment.objects.create(
                    project=project, employee_id=employee_id, role=role
                )

    def create(self, validated_data: dict) -> Project:
        assignments_data = validated_data.pop("employee_assignments", [])
        project = Project.objects.create(**validated_data)
        self._handle_assignments(project, assignments_data)
        return project

    def update(self, instance: Project, validated_data: dict) -> Project:
        assignments_data = validated_data.pop("employee_assignments", None)
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        if assignments_data is not None:
            instance.projectassignment_set.all().delete()
            self._handle_assignments(instance, assignments_data)
        return instance
