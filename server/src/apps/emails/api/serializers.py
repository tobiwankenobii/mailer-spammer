from rest_framework import serializers

from apps.emails.models import EmailConfig
from apps.users.models import User


class EmailConfigSerializer(serializers.ModelSerializer):
    """Serializer for CRUD operations on EmailConfig model."""

    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = EmailConfig
        fields = ("pk", "author", "recipient", "subject", "content")
