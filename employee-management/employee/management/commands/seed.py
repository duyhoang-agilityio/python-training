from django.core.management.base import BaseCommand
from employee.models import Department, Contact, Employee, Project, ProjectAssignment
from faker import Faker
import random


class Command(BaseCommand):
    help = "Seed database with sample data for Departments, Employees, Contacts, Projects, and ProjectAssignments."

    def handle(self, *args, **kwargs):
        fake = Faker()
        self.stdout.write("Seeding data...")

        # Clear existing data
        ProjectAssignment.objects.all().delete()
        Project.objects.all().delete()
        Contact.objects.all().delete()
        Employee.objects.all().delete()
        Department.objects.all().delete()

        # Create Departments
        departments = []
        for _ in range(5):
            dept = Department.objects.create(
                name=fake.company(),
                description=fake.catch_phrase(),
                code=fake.bothify(text="???-###"),
            )
            departments.append(dept)
        self.stdout.write(f"Created {len(departments)} departments.")

        # Create Employees
        status_choices = ["active", "inactive"]
        role_choices = ["Employee", "Manager", "Admin"]
        employees = []
        for _ in range(50):
            first_name = fake.first_name()
            last_name = fake.last_name()
            employee = Employee.objects.create(
                first_name=first_name,
                last_name=last_name,
                age=random.randint(20, 60),
                email=fake.unique.email(),
                birth_date=fake.date_of_birth(minimum_age=20, maximum_age=60),
                status=random.choice(status_choices),
                salary=round(random.uniform(30000, 120000), 2),
                department=random.choice(departments),
                role=random.choice(role_choices),
            )
            employees.append(employee)
        self.stdout.write(f"Created {len(employees)} employees.")

        # Create Contacts for each Employee (1-3 per employee)
        for emp in employees:
            for _ in range(random.randint(1, 3)):
                contact_type = random.choice(["phone", "email"])
                if contact_type == "phone":
                    value = fake.phone_number()
                else:
                    value = fake.email()
                Contact.objects.create(
                    employee=emp, contact_type=contact_type, value=value
                )
        self.stdout.write("Created contacts for employees.")

        # Create Projects
        projects = []
        for _ in range(5):
            project = Project.objects.create(
                name=fake.bs().title(), description=fake.text(max_nb_chars=200)
            )
            projects.append(project)
        self.stdout.write(f"Created {len(projects)} projects.")

        # Create ProjectAssignments: assign 1-5 random employees to each project
        for project in projects:
            num_assignments = random.randint(1, min(5, len(employees)))
            assigned_employees = random.sample(employees, num_assignments)
            for emp in assigned_employees:
                ProjectAssignment.objects.create(
                    project=project,
                    employee=emp,
                    role=random.choice(
                        ["Developer", "Tester", "Project Manager", "Designer"]
                    ),
                )
        self.stdout.write("Created project assignments for projects.")

        self.stdout.write(self.style.SUCCESS("Seeding complete!"))
