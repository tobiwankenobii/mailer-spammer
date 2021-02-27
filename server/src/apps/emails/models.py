from django.db import models


class EmailConfig(models.Model):
    """Config for building email templates"""

    title = models.CharField(max_length=127)
    content = models.TextField()
