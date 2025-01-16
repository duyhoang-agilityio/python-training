from django.contrib import admin
from .models import Department, Contact, Employee, Project, ProjectAssignment


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "age", "status", "department")
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("department",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


admin.site.register(Department)
admin.site.register(Contact)
admin.site.register(ProjectAssignment)
