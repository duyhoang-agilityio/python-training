from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

# Define a list of all module API URLs patterns
api_urlpatterns = [
    path("api/v1/", include("employee.urls")),
    path("api/v1/api-token-auth/", obtain_auth_token, name="api_token_auth"),
]
