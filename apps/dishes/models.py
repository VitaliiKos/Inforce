from django.db import models

from apps.restaurant.models import Restaurant
from utils.time_stamp import TimeStampedModel


class Dish(TimeStampedModel):
    """Model representing a dish."""
    CATEGORY_CHOICES = [
        ('first', 'Перші страви'),
        ('main', 'Основні страви'),
        ('garnish', 'Гарніри'),
        ('special', 'Страва дня'),
    ]

    class Meta:
        db_table = 'dish'
        ordering = ('id',)

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='dishes')

    def is_owner(self, user):
        return self.restaurant.is_owner(user)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
