from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from utils.time_stamp import TimeStampedModel

Employee = get_user_model()


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


class Menu(models.Model):
    class Meta:
        db_table = 'restaurant_menu'
        ordering = ('id',)

    date = models.DateField(default=timezone.now)
    dish = models.TextField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.restaurant.name}- {self.dish} - {self.date}"


class Vote(TimeStampedModel):
    class Meta:
        db_table = 'menu_vote'
        ordering = ('id',)

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, related_name='votes', on_delete=models.CASCADE)
