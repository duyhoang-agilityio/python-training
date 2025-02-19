from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/api-auth/login/")

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"detail": "Logged out successfully."})


# curl -X POST -H "Content-Type: application/json" \
# -d '{"username": "hoangduy", "password": "hoangduy"}' \
# http://127.0.0.1:8000/api-token-auth/


# curl -H "Authorization: Token your_generated_token_here" \
# http://127.0.0.1:8000/api/employees/
