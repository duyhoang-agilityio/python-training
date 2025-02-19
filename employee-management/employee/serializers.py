from rest_framework import serializers
from .models import Department, Contact, Employee, Project, ProjectAssignment


# ---------- Contact Serializer ----------
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "employee", "contact_type", "value"]


# ---------- Employee Serializer ----------
class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)

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


# ---------- Department Serializer ----------
class DepartmentSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ["id", "name", "description", "code", "employees", "employee_count"]

    def get_employee_count(self, obj):
        return obj.employees.count()


# ---------- ProjectAssignment Serializer ----------
class ProjectAssignmentSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source="employee", write_only=True
    )

    class Meta:
        model = ProjectAssignment
        fields = ["id", "employee", "employee_id", "role"]


# ---------- Project Serializer ----------
class ProjectSerializer(serializers.ModelSerializer):
    assignments = ProjectAssignmentSerializer(
        source="projectassignment_set", many=True, read_only=True
    )
    employee_assignments = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
        write_only=True,
        required=False,
        help_text="List of assignments, e.g. [{'employee': 1, 'role': 'Developer'}, ...]",
    )

    class Meta:
        model = Project
        fields = ["id", "name", "description", "assignments", "employee_assignments"]

    def validate_employee_assignments(self, value):
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

    def _handle_assignments(self, project, assignments_data):
        for assignment in assignments_data:
            employee_id = assignment.get("employee")
            role = assignment.get("role", "")
            if employee_id:
                ProjectAssignment.objects.create(
                    project=project, employee_id=employee_id, role=role
                )

    def create(self, validated_data):
        assignments_data = validated_data.pop("employee_assignments", [])
        project = Project.objects.create(**validated_data)
        self._handle_assignments(project, assignments_data)
        return project

    def update(self, instance, validated_data):
        assignments_data = validated_data.pop("employee_assignments", None)
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        if assignments_data is not None:
            instance.projectassignment_set.all().delete()
            self._handle_assignments(instance, assignments_data)
        return instance
