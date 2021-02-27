from django.db import models

from apps.users.models import User


class EmailConfig(models.Model):
    """Config for building email templates"""

    author = models.ForeignKey(
        User,
        related_name="email_configs",
        on_delete=models.CASCADE,
        editable=False,
    )
    recipient = models.EmailField()
    created_at = models.DateTimeField("Created at", auto_now_add=True)

    subject = models.CharField(max_length=127)
    content = models.TextField()
    send_at = models.DateTimeField()

    def __str__(self):
        return f"{self.subject} created_at {self.created_at}"
