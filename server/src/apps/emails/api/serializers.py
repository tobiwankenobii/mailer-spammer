from rest_framework import serializers

from apps.users.models import User
from ..models import EmailConfig, Image


class ImageSerializer(serializers.ModelSerializer):
    """Serializer for both write and read purposes, including files saving."""

    name = serializers.CharField()
    config = serializers.PrimaryKeyRelatedField(
        queryset=EmailConfig.objects.all(), write_only=True
    )

    class Meta:
        model = Image
        fields = ("pk", "name", "file", "config")


class EmailConfigSerializer(serializers.ModelSerializer):
    """Serializer for CRUD operations on EmailConfig model."""

    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, required=False
    )
    images = ImageSerializer(many=True, required=False)

    def create(self, validated_data):
        """Author should always be the user from the request.
        If images are present in initial_data they will get created right after config.
        """
        validated_data["author"] = self.context["request"].user
        instance = super().create(validated_data)
        if self.initial_data.get("images"):
            self.add_images(instance)
        return instance

    def update(self, instance, validated_data):
        """Author should never change through the request.
        Deletes all images and replaces them with incoming ones.
        """
        instance.images.delete()
        if self.initial_data.get("images"):
            self.add_images(instance)
        validated_data.pop("author", None)
        return super().update(instance, validated_data)

    def add_images(self, config: EmailConfig):
        """Builds image-like dicts from initial_data query_dict and creates Image instances."""
        images_data = [
            {"file": image, "name": image._name, "config": config.pk}
            for image in self.initial_data.getlist("images")
        ]
        serializer = ImageSerializer(data=images_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    class Meta:
        model = EmailConfig
        fields = (
            "pk",
            "author",
            "recipient",
            "subject",
            "content",
            "send_at",
            "images",
        )
