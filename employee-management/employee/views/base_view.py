from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsManager


class BaseViewSet(viewsets.ModelViewSet):
    """
    Base viewset that centralizes permission logic.
    Write actions (create, update, partial_update, destroy)
    require IsAuthenticated and IsManager, while read actions
    use a default read permission class.
    """

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
