from django.contrib import admin
from .models import Department, Contact, Employee, Project, ProjectAssignment

from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Employee model.
    Displays the full name, age, status, and department in the list view.
    Provides search functionality on first and last names.
    Filters employees by department and status.
    """

    list_display = ("full_name", "age", "status", "department", "role", "user")
    search_fields = ("first_name", "last_name")
    list_filter = ("department", "status")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Project model.
    Displays the project name and description in the list view.
    """

    list_display = ("name", "description")


admin.site.register(Department)
admin.site.register(Contact)
admin.site.register(ProjectAssignment)
