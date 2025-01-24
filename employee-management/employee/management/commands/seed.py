# employee/management/commands/seed
from django.core.management.base import BaseCommand
from employee.models import Department, Project, Employee


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        # Create Departments
        departments = ["HR", "Engineering", "Marketing"]
        department_objs = []  # Store created departments
        for dept in departments:
            department_obj, _ = Department.objects.get_or_create(name=dept)
            department_objs.append(department_obj)

        # Create Projects
        for i in range(1, 6):
            Project.objects.get_or_create(
                name=f"Project {i}", description=f"Description of Project {i}"
            )

        # Create Employees
        for i in range(1, 11):
            department = department_objs[i % len(department_objs)]
            Employee.objects.get_or_create(
                first_name=f"First{i}",
                last_name=f"Last{i}",
                department=department,
                age=20 + i,
                status="Active" if i % 2 == 0 else "Inactive",
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded data!"))
