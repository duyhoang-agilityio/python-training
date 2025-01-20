from django.core.management.base import BaseCommand
from core.models import Employee


class Command(BaseCommand):
    help = "Combine first_name and last_name into full_name"

    def handle(self, *args, **kwargs):
        employees = Employee.objects.all()
        for employee in employees:
            self.stdout.write(f"Full Name: {employee.full_name}")
