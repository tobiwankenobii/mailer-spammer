import os

from sendgrid import Mail, SendGridAPIClient

from apps.emails.models import EmailConfig


class SendGridEmailService:
    """Service for handling email building & sending using SendGrid API."""

    def __init__(self):
        self.sender = os.environ.get("SENDGRID_EMAIL")
        self.api_key = os.environ.get("SENDGRID_API_KEY")

    def build_email(self, config: EmailConfig) -> Mail:
        """Builds an email based on given config.
        Edits email's sending date if config has one, otherwise email will be send immediately.
        """
        mail = Mail(
            from_email=self.sender,
            to_emails=config.recipient,
            subject=config.subject,
            html_content=config.content,
        )
        if config.send_at:
            mail.send_at = int(config.send_at.timestamp())
        if config.images:
            mail.attachment = [
                image.to_attachment() for image in config.images.all()
            ]
        return mail

    def send_email(self, mail: Mail):
        sg = SendGridAPIClient(self.api_key)
        sg.send(mail)

    def build_and_send_email(self, config: EmailConfig):
        mail = self.build_email(config)
        self.send_email(mail)
