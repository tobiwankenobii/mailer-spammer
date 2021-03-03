from django.db import models


class ImageManager(models.Manager):
    """Overrides base manager just to clear files after whole queryset getting deleted."""

    def delete(self):
        for image in self.get_queryset():
            image.delete()
