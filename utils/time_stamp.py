from django.db import models


class TimeStampedModel(models.Model):
    """An abstract base model for adding timestamp fields."""

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
