from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeViewSet,
    DepartmentViewSet,
    ContactViewSet,
    ProjectViewSet,
    CustomLogoutView,
)

router = DefaultRouter()
router.register("employees", EmployeeViewSet, basename="employee")
router.register("departments", DepartmentViewSet, basename="department")
router.register("contacts", ContactViewSet, basename="contact")
router.register("projects", ProjectViewSet, basename="project")

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("api-auth/custom-logout/", CustomLogoutView.as_view(), name="custom-logout"),
]
