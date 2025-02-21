from rest_framework import filters
from rest_framework import status
from core.base_view import BaseViewSet
from .models import Employee, Contact, Department, Project, ProjectAssignment
from .serializers import (
    EmployeeSerializer,
    ContactSerializer,
    DepartmentSerializer,
    ProjectSerializer,
)
from .permissions import EmployeeAccessPermission
from rest_framework.decorators import action
from rest_framework.response import Response


class EmployeeViewSet(BaseViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["first_name", "last_name", "age"]
    search_fields = ["first_name", "last_name", "email"]
    filterset_fields = {"birth_date": ["gte", "lte"]}

    # For read actions, allow managers or the employee themself.
    read_permission_classes = [EmployeeAccessPermission]

    def get_queryset(self):
        user = self.request.user
        # If the user is not authenticated, return an empty queryset
        if not user.is_authenticated:
            return Employee.objects.none()
        # If the user is a manager or admin, they can see all employees.
        if user.is_manager_or_admin():
            return Employee.objects.all()
        # Otherwise, if the user is an employee, return only their record.
        if user.is_employee():
            return Employee.objects.filter(user=user)
        # Optionally, for any other case, return an empty queryset:
        return Employee.objects.none()


class ContactViewSet(BaseViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_manager_or_admin():
            return Contact.objects.all()

        return Contact.objects.filter(employee__user=user)


class DepartmentViewSet(BaseViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_manager_or_admin():
            return Department.objects.all()

        return Department.objects.filter(employees__user=user).distinct()

    @action(detail=True, methods=["post"], url_path="add-employees")
    def add_employees(self, request, pk=None):
        department = self.get_object()
        employee_ids = request.data.get("employee_ids", [])
        if not isinstance(employee_ids, list):
            return Response(
                {"error": "employee_ids must be a list."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        employees = Employee.objects.filter(id__in=employee_ids)
        for emp in employees:
            emp.department = department
            emp.save()
        serializer = self.get_serializer(department)
        return Response(serializer.data)


class ProjectViewSet(BaseViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_manager_or_admin():
            return Project.objects.all()

        return Project.objects.filter(
            projectassignment__employee__email=user.email
        ).distinct()

    @action(detail=True, methods=["post"], url_path="assign-employees")
    def assign_employees(self, request, pk=None):
        project = self.get_object()
        assignments = request.data.get("assignments", [])
        if not isinstance(assignments, list):
            return Response(
                {"error": "assignments must be a list."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for assignment in assignments:
            employee_id = assignment.get("employee")
            role = assignment.get("role", "")
            if employee_id:
                ProjectAssignment.objects.create(
                    project=project, employee_id=employee_id, role=role
                )
        serializer = self.get_serializer(project)
        return Response(serializer.data)
