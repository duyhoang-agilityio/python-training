from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from .base_view import BaseViewSet
from ..models import Department, Employee
from ..serializers import DepartmentSerializer


class DepartmentViewSet(BaseViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Department.objects.all()
        # Non-staff: show only departments with an employee whose email matches.
        return Department.objects.filter(employees__email=user.email).distinct()

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
