from rest_framework import permissions


class IsManagerOrEmployeeItself(permissions.BasePermission):
    """
    Allow managers and admins full access; employees can only access their own record.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Use the custom role methods
        if user.is_manager() or user.is_admin():
            return True

        # Regular employees can only access their own record.
        return obj.email == user.email
