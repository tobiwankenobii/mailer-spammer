from rest_framework import viewsets

from apps.emails.models import EmailConfig
from .serializers import EmailConfigSerializer


class EmailConfigManagementViewSet(viewsets.ModelViewSet):
    """CRUD manager for the EmailConfig model."""

    queryset = EmailConfig.objects.all().order_by("created_at")
    serializer_class = EmailConfigSerializer

    def get_queryset(self):
        """Show configs created only by giver user."""
        return self.queryset.filter(author=self.request.user)

    def create(self, request, *args, **kwargs):
        """Take the author field from the request."""
        request.data["author"] = request.user.pk
        return super().create(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        """Do not allow overwriting initial author."""
        request.data.pop("author")
        return super().update(request, args, kwargs)
