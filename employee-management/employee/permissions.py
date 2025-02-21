from rest_framework import permissions


class IsManagerOrAdmin(permissions.BasePermission):
    """Global permission check for manager or admin role"""

    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_manager_or_admin()


class IsEmployeeOwner(permissions.BasePermission):
    """Object-level permission for employee-owned resources"""

    def has_object_permission(self, request, view, obj):
        # Employee can only access their own records
        return obj.user == request.user and request.user.is_employee()


class EmployeeAccessPermission(permissions.BasePermission):
    """Combined permission for employee-related operations"""

    def has_permission(self, request, view):
        if view.action in ["create", "update", "destroy"]:
            return request.user.is_manager_or_admin()
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_manager_or_admin():
            return True
        return obj.user == request.user and request.user.is_employee()
