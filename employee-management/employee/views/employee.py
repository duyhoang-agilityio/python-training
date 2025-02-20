from rest_framework import filters
from .base_view import BaseViewSet
from ..models import Employee
from ..serializers import EmployeeSerializer
from ..permissions import IsManagerOrEmployeeItself


class EmployeeViewSet(BaseViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["first_name", "last_name", "age"]
    search_fields = ["first_name", "last_name", "email"]
    filterset_fields = {"birth_date": ["gte", "lte"]}

    # For read actions, allow managers or the employee themself.
    read_permission_classes = [IsManagerOrEmployeeItself]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Employee.objects.all()
        # Non-staff: filter by matching email.
        return Employee.objects.filter(email=user.email)
