from rest_framework import serializers

from apps.emails.models import EmailConfig
from apps.users.models import User


class EmailConfigSerializer(serializers.ModelSerializer):
    """Serializer for CRUD operations on EmailConfig model."""

    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, required=False
    )

    def create(self, validated_data):
        """Author should always be the user from the request."""
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """And he should never change through the request."""
        validated_data.pop("author")
        return super().update(instance, validated_data)

    class Meta:
        model = EmailConfig
        fields = ("pk", "author", "recipient", "subject", "content", "send_at")
