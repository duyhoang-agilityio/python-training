from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class BasePaginationTest(APITestCase):
    __test__ = False

    # Subclasses must define:
    url_basename = None
    page_size = 10  # Default page size

    def get_list_url(self):
        return reverse(f"{self.url_basename}-list")

    def test_pagination(self):
        url = self.get_list_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertLessEqual(len(response.data["results"]), self.page_size)
