from django.core.management.base import BaseCommand
from employee.models import Employee
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Combine first_name and last_name into full_name"

    def handle(self, *args, **kwargs):
        employees = Employee.objects.all()
        if not employees.exists():
            self.stdout.write("No employees found in the database.")
            return

        for employee in employees:
            self.stdout.write(f"Full Name: {employee.full_name} {employee.role}")

        self.stdout.write("Command completed successfully.")
