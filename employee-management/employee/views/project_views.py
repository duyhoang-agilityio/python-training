from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from .base_view import BaseViewSet
from ..models import Project, ProjectAssignment
from ..serializers import ProjectSerializer


class ProjectViewSet(BaseViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Project.objects.all()
        # Non-staff: return projects assigned to an employee with matching email.
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
