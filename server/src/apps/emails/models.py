from django.db import models

from apps.emails.managers import ImageManager
from apps.users.models import User


class EmailConfig(models.Model):
    """Config for building email templates."""

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
    send_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.subject} created_at {self.created_at}"


class Image(models.Model):
    """Makes the config capable of storing multiple image files."""

    name = models.CharField(max_length=127)
    file = models.ImageField(upload_to="images/")
    config = models.ForeignKey(
        EmailConfig, on_delete=models.CASCADE, related_name="images"
    )

    objects = ImageManager()

    def delete(self, using=None, keep_parents=False):
        """Delete image file on instance destroy."""
        self.file.storage.delete(self.file.name)
        super().delete(using, keep_parents)

    def __str__(self):
        return self.name
