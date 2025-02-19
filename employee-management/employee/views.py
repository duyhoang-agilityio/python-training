from rest_framework import viewsets, filters, status
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token

from .models import Employee, Department, Contact, Project, ProjectAssignment
from .serializers import (
    EmployeeSerializer,
    DepartmentSerializer,
    ContactSerializer,
    ProjectSerializer,
    ProjectAssignmentSerializer,
)
from .permissions import IsManager, IsManagerOrEmployeeItself


# --- BaseViewSet for common permission logic ---
class BaseViewSet(viewsets.ModelViewSet):
    # Define which actions require "write" permissions
    write_actions = ["create", "update", "partial_update", "destroy"]

    def get_permissions(self):
        if self.action in self.write_actions:
            permission_classes = getattr(
                self, "write_permission_classes", [IsAuthenticated, IsManager]
            )
        else:
            permission_classes = getattr(
                self, "read_permission_classes", [IsAuthenticated]
            )
        return [permission() for permission in permission_classes]


# --- Employee ViewSet ---
class EmployeeViewSet(BaseViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["first_name", "last_name", "age"]
    search_fields = ["first_name", "last_name", "email"]
    filterset_fields = {"birth_date": ["gte", "lte"]}

    # For read actions, allow managers/admins or the employee themself.
    read_permission_classes = [IsAuthenticated, IsManagerOrEmployeeItself]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Employee.objects.all()
        # Non-staff users see only their own record (matched by email)
        return Employee.objects.filter(email=user.email)


# --- Department ViewSet ---
class DepartmentViewSet(BaseViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    # For read actions, only authenticated users are required.
    read_permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Department.objects.all()
        # Non-staff: show only departments that include an employee with a matching email.
        return Department.objects.filter(employees__email=user.email).distinct()

    # Custom action to add multiple employees to a department.
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


# --- Contact ViewSet ---
class ContactViewSet(BaseViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    read_permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Contact.objects.all()
        # Non-staff: only show contacts for employees with a matching email.
        return Contact.objects.filter(employee__email=user.email)


# --- Project ViewSet ---
class ProjectViewSet(BaseViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    read_permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Project.objects.all()
        # Non-staff: show projects assigned to an employee with matching email.
        return Project.objects.filter(
            projectassignment__employee__email=user.email
        ).distinct()

    # Custom action to assign employees to a project.
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


# --- Custom Logout Endpoint ---
class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/api-auth/login/")

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"detail": "Logged out successfully."})


# curl -X POST -H "Content-Type: application/json" \
# -d '{"username": "hoangduy", "password": "hoangduy"}' \
# http://127.0.0.1:8000/api-token-auth/


# curl -H "Authorization: Token your_generated_token_here" \
# http://127.0.0.1:8000/api/employees/
