from employee.models import Department, Employee
from tests.base_crud_test import BaseCRUDTest
from tests.base_searching_test import BaseSearchingTest
from tests.base_pagination_test import BasePaginationTest

class DepartmentOrderingTest(BaseOrderingTest):
    url_basename = "department"
    ordering_field = "first_name"

    def setUp(self):
        super().setUp()
        # Authenticate the client.
        admin_dept = Department.objects.create(name="Admin Dept", description="Admin Dept", code="ADM")
        admin_user = Employee.objects.create_superuser(
            email="admin2@example.com",
            password="password123",
            first_name="Admin",
            last_name="User",
            age=30,
            status="Active",
            department=admin_dept,
            role="admin",
        )
        self.client.force_authenticate(user=admin_user)

class DepartmentSearchingTest(BaseSearchingTest):
    url_basename = "department"
    search_query = "HR"
    search_field = "name"

    def setUp(self):
        super().setUp()
        admin_dept = Department.objects.create(name="Admin Dept", description="Admin Dept", code="ADM")
        admin_user = Employee.objects.create_superuser(
            email="admin3@example.com",
            password="password123",
            first_name="Admin",
            last_name="User",
            age=30,
            status="Active",
            department=admin_dept,
            role="admin",
        )
        # Create a couple of departments
        Department.objects.create(name="HR Department", description="Handles HR", code="HR01")
        Department.objects.create(name="Finance Department", description="Handles finance", code="FIN")
        self.client.force_authenticate(user=admin_user)

class DepartmentPaginationTest(BasePaginationTest):
    url_basename = "department"
    page_size = 10

    def setUp(self):
        super().setUp()        
        admin_dept = Department.objects.create(name="Admin Dept", description="Admin Dept", code="ADM")
        admin_user = Employee.objects.create_superuser(
            email="admin4@example.com",
            password="password123",
            first_name="Admin",
            last_name="User",
            age=30,
            status="Active",
            department=admin_dept,
            role="admin",
        )
        # Create several departments for pagination.
        for i in range(15):
            Department.objects.create(
                name=f"Department {i}",
                description="Test department",
                code=f"DPT{i}"
            )
        self.client.force_authenticate(user=admin_user)