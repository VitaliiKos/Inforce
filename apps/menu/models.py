from django.db import models
from datetime import date

from apps.dishes.models import Dish
from apps.restaurant.models import Restaurant
from utils.time_stamp import TimeStampedModel


class DailyMenu(TimeStampedModel):
    """Model representing a daily menu for a restaurant."""

    class Meta:
        db_table = 'menu'
        ordering = ('-date',)
        unique_together = ('date',)

    dishes = models.ManyToManyField(Dish, related_name='menus')
    date = models.DateField(default=date.today)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')

    def __str__(self):
        return f"Menu for {self.date}"
