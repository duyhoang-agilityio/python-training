from rest_framework import permissions
from .models import Employee


class IsManagerOrAdmin(permissions.BasePermission):
    """Global permission check for manager or admin role"""

    def has_permission(self, request, view):
        return request.user.is_superuser or Employee.is_manager_or_admin(request.user)


class IsEmployeeOwner(permissions.BasePermission):
    """Object-level permission for employee-owned resources"""

    def has_object_permission(self, request, view, obj):
        # Employee can only access their own records
        return obj.user == request.user and Employee.is_employee(request.user)


class EmployeeAccessPermission(permissions.BasePermission):
    """Combined permission for employee-related operations"""

    def has_permission(self, request, view):
        if view.action in ["create", "update", "destroy"]:
            return Employee.is_manager_or_admin(request.user)
        return True

    def has_object_permission(self, request, view, obj):
        if Employee.is_manager_or_admin(request.user):
            return True
        return obj.user == request.user and Employee.is_employee(request.user)
