from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from utils.time_stamp import TimeStampedModel

Employee = get_user_model()


def get_current_date():
    return timezone.now().date()


class Restaurant(TimeStampedModel):
    """Model representing a restaurant."""

    class Meta:
        db_table = 'restaurant'
        ordering = ('id',)

    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def is_owner(self, user):
        """Check if the given user is the owner of the restaurant."""
        return self.owner == user
