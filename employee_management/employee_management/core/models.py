from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Manager, QuerySet


class EmployeeQuerySet(QuerySet):
    def active(self):
        return self.filter(status="Active")


class EmployeeManager(Manager):
    def aged_over_25(self):
        return self.filter(age__gt=25)

    def get_queryset(self):
        return EmployeeQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Contact(models.Model):
    employee = models.ForeignKey(
        "Employee", related_name="contacts", on_delete=models.CASCADE
    )
    address = models.TextField()

    def __str__(self):
        return f"Contact for {self.employee}"


class Employee(models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    department = models.ForeignKey(
        Department, related_name="employees", on_delete=models.SET_NULL, null=True
    )
    objects = EmployeeManager.from_queryset(EmployeeQuerySet)()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProjectAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.employee.full_name} -> {self.project.name}"


@receiver(post_save, sender=Project)
def add_high_role_members(sender, instance, created, **kwargs):
    if created:
        high_role_employees = Employee.objects.filter(status="Active")[:3]
        for employee in high_role_employees:
            ProjectAssignment.objects.create(
                employee=employee, project=instance, role="High Role"
            )
