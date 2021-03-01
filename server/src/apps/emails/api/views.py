from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import EmailConfigSerializer
from ..models import EmailConfig
from ..services import SendGridEmailService


class EmailConfigManagementViewSet(viewsets.ModelViewSet):
    """CRUD manager for the EmailConfig model."""

    queryset = EmailConfig.objects.all().order_by("created_at")
    serializer_class = EmailConfigSerializer

    def get_queryset(self):
        """Show configs created only by given user."""
        return self.queryset.filter(author=self.request.user)

    @action(detail=True, methods=["get"])
    def send(self, request, pk):
        """Builds and sends an email using Sendgrid Service based on EmailConfig instance."""
        config = self.get_object()
        SendGridEmailService().build_and_send_email(config)
        return Response(
            status=200, data={"detail": "Mail has been sent successfully"}
        )
