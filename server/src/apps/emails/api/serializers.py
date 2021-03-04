from rest_framework import serializers

from apps.users.models import User
from ..models import EmailConfig, Image, RssLink


class RssLinkSerializer(serializers.ModelSerializer):
    """Serializer for both write and read purposes."""

    config = serializers.PrimaryKeyRelatedField(
        queryset=EmailConfig.objects.all(), write_only=True
    )

    class Meta:
        model = RssLink
        fields = ("pk", "url", "config")


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
    rss_links = RssLinkSerializer(many=True, required=False)

    def create(self, validated_data):
        """Author should always be the user from the request.
        If images or rss_links are present in initial_data they will get created right after config.
        """
        validated_data["author"] = self.context["request"].user
        instance = super().create(validated_data)
        self._add_related_instances(instance)
        return instance

    def update(self, instance, validated_data):
        """Author should never change through the request.
        Deletes all images and rss_links and replaces them with incoming ones.
        """
        instance.images.delete()
        instance.rss_links.all().delete()
        self._add_related_instances(instance)
        validated_data.pop("author", None)
        return super().update(instance, validated_data)

    def _add_related_instances(self, config: EmailConfig):
        if self.initial_data.get("images"):
            self._add_images(config)
        if self.initial_data.get("rss_links"):
            self._add_links(config)

    def _add_images(self, config: EmailConfig):
        """Builds image-like dicts from initial_data query_dict and creates Image instances."""
        images_data = [
            {"file": image, "name": image._name, "config": config.pk}
            for image in self.initial_data.getlist("images")
        ]
        serializer = ImageSerializer(data=images_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def _add_links(self, config: EmailConfig):
        """Retrieves RSS links from data and creates models for storing them."""
        links_data = [
            {"url": link, "config": config.pk}
            for link in self.initial_data.getlist("rss_links")
        ]
        serializer = RssLinkSerializer(data=links_data, many=True)
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
            "rss_links",
        )
