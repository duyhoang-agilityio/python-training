from django.db import models
from django.db.models import Manager, QuerySet
from .base_model import BaseModel


class EmployeeQuerySet(QuerySet):
    """
    Custom queryset for the Employee model to add reusable filtering logic.
    """

    def active(self) -> QuerySet["Employee"]:
        """
        Filters employees with status set to 'Active'.

        Returns:
            QuerySet: A queryset of active employees.
        """
        return self.filter(status="Active")


class EmployeeManager(Manager):
    """
    Custom manager for the Employee model to provide additional query methods.
    """

    def aged_over_25(self) -> QuerySet["Employee"]:
        """
        Filters employees who are older than 25.

        Returns:
            QuerySet: A queryset of employees aged over 25.
        """
        return self.filter(age__gt=25)


class Department(BaseModel):
    """
    Represents a department in the organization.
    """

    name = models.CharField(
        max_length=100,
        help_text="Name of the department.",
    )
    code = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Contact(BaseModel):
    """
    Stores contact details associated with an employee.
    """

    employee = models.ForeignKey(
        "Employee",
        related_name="contacts",
        on_delete=models.CASCADE,
        help_text="The employee associated with this contact.",
    )
    address = models.TextField(help_text="The contact address of the employee.")

    def __str__(self) -> str:
        return f"Contact for {self.employee}"


class Employee(BaseModel):
    """
    Employee model to store employee details.

    Attributes:
        first_name (CharField): The first name of the employee.
        last_name (CharField): The last name of the employee.
        age (PositiveIntegerField): The age of the employee.
        status (CharField): The employment status of the employee.
        salary (DecimalField): The salary of the employee.
        department (ForeignKey): The department where the employee works.
        role (CharField): The role of the employee.
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

    first_name = models.CharField(
        max_length=50, help_text="The first name of the employee."
    )
    last_name = models.CharField(
        max_length=50, help_text="The last name of the employee."
    )
    age = models.PositiveIntegerField(help_text="The age of the employee.")
    email = models.CharField(
        max_length=50,
        help_text="The email of the employee.",
        default="example@example.com",
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        help_text="The employment status of the employee.",
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        help_text="The salary of the employee.",
    )
    department = models.ForeignKey(
        Department,
        related_name="employees",
        on_delete=models.SET_NULL,
        null=True,
        help_text="The department where the employee works.",
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default="Employee",
        help_text="The role of the employee.",
    )

    objects = EmployeeManager.from_queryset(EmployeeQuerySet)()

    @property
    def full_name(self) -> str:
        """
        Returns the full name of the employee by combining first and last names.
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name


class Project(BaseModel):
    """
    Represents a project in the organization.
    """

    name = models.CharField(max_length=100, help_text="The name of the project.")
    description = models.TextField(help_text="The description of the project.")

    def __str__(self) -> str:
        return self.name


class ProjectAssignment(BaseModel):
    """
    Links an employee to a project with a specific role.
    """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        help_text="The employee assigned to the project.",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        help_text="The project to which the employee is assigned.",
    )
    role = models.CharField(
        max_length=100, help_text="The role of the employee in the project."
    )

    def __str__(self) -> str:
        return f"{self.employee.full_name} -> {self.project.name}"
