from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Manager, QuerySet


class EmployeeQuerySet(QuerySet):
    """
    Custom queryset for the Employee model to add reusable filtering logic.
    """
    def active(self):
        """
        Filters employees with 'Active' status.
        """
        return self.filter(status="Active")


class EmployeeManager(Manager):
    """
    Custom manager for the Employee model to provide additional query methods.
    """
    def aged_over_25(self):
        """
        Filters employees who are older than 25 years.
        """
        return self.filter(age__gt=25)


class Department(models.Model):
    """
    Represents a department in the organization.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Contact(models.Model):
    """
    Stores contact details associated with an employee.
    """
    employee = models.ForeignKey(
        "Employee", related_name="contacts", on_delete=models.CASCADE
    )
    address = models.TextField()

    def __str__(self):
        return f"Contact for {self.employee}"


class Employee(models.Model):
    """
    Represents an employee in the organization, including their details and relationships.
    """
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Manager", "Manager"),
        ("Employee", "Employee"),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    department = models.ForeignKey(
        Department, related_name="employees", on_delete=models.SET_NULL, null=True
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="Employee")

    objects = EmployeeManager.from_queryset(EmployeeQuerySet)()

    @property
    def full_name(self):
        """
        Returns the full name of the employee by combining first and last names.
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Project(models.Model):
    """
    Represents a project in the organization.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProjectAssignment(models.Model):
    """
    Links an employee to a project with a specific role.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.employee.full_name} -> {self.project.name}"


@receiver(post_save, sender=Project)
def add_high_role_members(sender, instance, created, **kwargs):
    """
    Signal handler that assigns 'Admin' employees to a newly created project.

    Args:
        sender (Model): The model class sending the signal.
        instance (Project): The project instance being saved.
        created (bool): Whether the project was created (True) or updated (False).
        **kwargs: Additional keyword arguments.
    """
    if created:
        highest_role = "Admin"

        # Get active employees with the highest role
        high_role_employees = Employee.objects.filter(
            status="Active", role=highest_role
        )

        # Add these employees to the project
        for employee in high_role_employees:
            ProjectAssignment.objects.create(
                employee=employee, project=instance, role=highest_role
            )
