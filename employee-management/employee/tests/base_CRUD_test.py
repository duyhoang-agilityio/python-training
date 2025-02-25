from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class BaseCRUDTest(APITestCase):
    __test__ = False  # prevent pytest from discovering this as a test case

    # Subclasses must define:
    #   model: the Django model class to test.
    #   url_basename: the basename used in the router (e.g. "department")
    #   create_data: a dict with valid data for creating an instance.
    #   update_data: a dict with fields to update on an instance.
    model = None
    url_basename = None
    create_data = {}
    update_data = {}

    def get_list_url(self):
        return reverse(f"{self.url_basename}-list")

    def get_detail_url(self, pk):
        return reverse(f"{self.url_basename}-detail", args=[pk])

    def test_create(self):
        response = self.client.post(
            self.get_list_url(), self.create_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in self.create_data.items():
            self.assertEqual(response.data.get(key), value)

    def test_read_list(self):
        instance = self.model.objects.create(**self.create_data)
        response = self.client.get(self.get_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            any(item["id"] == instance.id for item in response.data.get("results", []))
        )

    def test_read_detail(self):
        instance = self.model.objects.create(**self.create_data)
        response = self.client.get(self.get_detail_url(instance.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, value in self.create_data.items():
            self.assertEqual(response.data.get(key), value)

    def test_update(self):
        instance = self.model.objects.create(**self.create_data)
        response = self.client.patch(
            self.get_detail_url(instance.pk), self.update_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, value in self.update_data.items():
            self.assertEqual(response.data.get(key), value)

    def test_delete(self):
        instance = self.model.objects.create(**self.create_data)
        response = self.client.delete(self.get_detail_url(instance.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.model.objects.filter(pk=instance.pk).exists())
