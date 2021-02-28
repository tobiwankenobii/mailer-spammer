import os

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from apps.emails.models import EmailConfig
from .serializers import EmailConfigSerializer


class EmailConfigManagementViewSet(viewsets.ModelViewSet):
    """CRUD manager for the EmailConfig model."""

    queryset = EmailConfig.objects.all().order_by("created_at")
    serializer_class = EmailConfigSerializer

    def get_queryset(self):
        """Show configs created only by given user."""
        return self.queryset.filter(author=self.request.user)

    @action(detail=True, methods=["get"])
    def send(self, request, pk):
        """Builds and sends an email using Sendgrid based on EmailConfig instance."""
        config = self.get_object()
        message = Mail(
            from_email=os.environ.get("SENDGRID_EMAIL"),
            to_emails=config.recipient,
            subject=config.subject,
            html_content=config.content,
        )
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        sg.send(message)
        return Response(
            status=200, data={"detail": "Mail has been sent successfully"}
        )
