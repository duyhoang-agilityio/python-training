from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
)
from django.core.validators import MinValueValidator
from .base_model import BaseModel
from .constants import STATUS_CHOICES, ROLE_CHOICES, CONTACT_TYPE_CHOICES


# ---------- Department ----------
class Department(BaseModel):
    """
    Represents a department in the organization.
    """

    name = models.CharField(
        max_length=100,
        help_text="Name of the department.",
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the department.",
    )
    code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="Optional department code.",
    )

    def __str__(self) -> str:
        return self.name


# ---------- Contact ----------
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
    contact_type = models.CharField(
        max_length=20,
        choices=CONTACT_TYPE_CHOICES,
        help_text="The type of contact (e.g., phone, email).",
        null=True,
        blank=True,
    )
    value = models.CharField(
        max_length=255,
        help_text="The contact value (phone number or email address).",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.contact_type} for {self.employee}"


# ---------- Employee ----------
class Employee(AbstractBaseUser, PermissionsMixin):
    """
    Employee model to store employee details.

    Attributes:
        first_name (CharField): The first name of the employee.
        last_name (CharField): The last name of the employee.
        age (PositiveIntegerField): The age of the employee.
        email (EmailField): The email of the employee.
        birth_date (DateField): The birth date of the employee.
        status (CharField): The employment status.
        salary (DecimalField): The salary.
        department (ForeignKey): The department where the employee works.
        role (CharField): The role of the employee.
    """

    first_name = models.CharField(
        max_length=50, help_text="The first name of the employee."
    )
    last_name = models.CharField(
        max_length=50, help_text="The last name of the employee."
    )
    age = models.PositiveIntegerField(
        help_text="The age of the employee.",
        default=25,
        validators=[MinValueValidator(18)],
    )
    email = models.EmailField(
        max_length=50,
        help_text="The email of the employee.",
        default="example@example.com",
        unique=True,
    )
    birth_date = models.DateField(
        null=True, blank=True, help_text="The birth date of the employee."
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

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def is_manager_or_admin(self) -> bool:
        """Return True if the user is either a manager or an admin."""
        return self.role.lower() in {"manager", "admin"}

    def is_employee(self) -> bool:
        """Check if user has employee role"""
        return self.role.lower() == "employee"

    @property
    def full_name(self) -> str:
        """
        Returns the full name of the employee by combining first and last names.
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name


# ---------- Project ----------
class Project(BaseModel):
    """
    Represents a project in the organization.
    """

    name = models.CharField(max_length=100, help_text="The name of the project.")
    description = models.TextField(help_text="The description of the project.")

    def __str__(self) -> str:
        return self.name


# ---------- ProjectAssignment ----------
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
