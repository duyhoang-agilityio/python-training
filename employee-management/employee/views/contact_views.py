from .base_view import BaseViewSet
from ..models import Contact
from ..serializers import ContactSerializer


class ContactViewSet(BaseViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Contact.objects.all()
        # Non-staff: show only contacts for employees with a matching email.
        return Contact.objects.filter(employee__email=user.email)
