from django.core.management.base import BaseCommand
from core.models import Department, Project, Employee


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Create Departments
        departments = ["HR", "Engineering", "Marketing"]
        for dept in departments:
            Department.objects.get_or_create(name=dept)

        # Create Projects
        for i in range(1, 6):
            Project.objects.get_or_create(
                name=f"Project {i}", description=f"Description of Project {i}"
            )

        # Create Employees
        for i in range(1, 11):
            Employee.objects.get_or_create(
                first_name=f"First{i}",
                last_name=f"Last{i}",
                department_id=(i % 3) + 1,  # Assign departments cyclically
                age=20 + i,
                status="Active" if i % 2 == 0 else "Inactive",
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded data!"))
