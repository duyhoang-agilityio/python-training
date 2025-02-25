import pytest
from employee.serializers import EmployeeSerializer


@pytest.mark.django_db
class TestEmployeeSerializerValidation:
    def test_invalid_email(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
            "email": "not-an-email",
            "status": "Active",
        }
        serializer = EmployeeSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_missing_required_fields(self):
        data = {"age": 30, "status": "Active"}
        serializer = EmployeeSerializer(data=data)
        assert not serializer.is_valid()
        assert "first_name" in serializer.errors
        assert "last_name" in serializer.errors
