from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer


class UserRegisterView(generics.CreateAPIView):
    """View for user registration."""

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
