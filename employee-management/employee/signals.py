from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project, Employee, ProjectAssignment


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
        # Get active employees with the highest role
        high_role_employees = Employee.objects.filter(
            role__iexact="admin"
        ) | Employee.objects.filter(role__iexact="manager")

        # Add these employees to the project
        for employee in high_role_employees:
            ProjectAssignment.objects.create(
                employee=employee, project=instance, role="Auto-assigned"
            )
