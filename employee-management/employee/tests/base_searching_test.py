from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class BaseSearchingTest(APITestCase):
    __test__ = False

    # Subclasses must define:
    url_basename = None
    search_query = None   
    search_field = None   

    def get_list_url(self, query_params=""):
        return reverse(f"{self.url_basename}-list") + query_params

    def test_searching(self):
        url = self.get_list_url(f"?search={self.search_query}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", [])
        self.assertTrue(
            any(self.search_query in item[self.search_field] for item in results)
        )

class BaseOrderingTest(APITestCase):
    __test__ = False

    url_basename = None
    ordering_field = None  

    def get_list_url(self, query_params=""):
        return reverse(f"{self.url_basename}-list") + query_params

    def test_ordering(self):
        url = self.get_list_url(f"?ordering={self.ordering_field}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Extract the field values from the response results.
        field_values = [item[self.ordering_field] for item in response.data.get("results", [])]
        self.assertEqual(field_values, sorted(field_values))
