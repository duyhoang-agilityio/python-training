from rest_framework import permissions


class IsManager(permissions.BasePermission):
    """
    Only allow access if the user is a manager/admin (staff).
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsManagerOrEmployeeItself(permissions.BasePermission):
    """
    Allow managers full access; employees can only access their own record.
    """

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        # For non-staff users, allow if employee email matches the user email.
        return obj.email == request.user.email
