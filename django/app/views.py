"""
For more information on setting up DRF views see docs:
https://www.django-rest-framework.org/api-guide/views/#class-based-views
"""

import logging

from app import throttles
from app.session import SessionAPI
from app.tasks import greeting_task
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import login

logger = logging.getLogger(__name__)


class LoginView(KnoxLoginView):
    """
    Login view for the API.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        """
        Login view for the API.
        """
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class APISessionView(APIView):
    session: SessionAPI

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.session = SessionAPI(request)


class ExampleView(APISessionView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttles.BurstUserRateThrottle]

    def get(self, request, format=None):
        name = self.request.query_params.get("name") or "world"
        greeting_task.delay(name)
        return Response({"greeting": f"Hello, {name}!"})