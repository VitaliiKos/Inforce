from django.contrib import admin

from .models import Dish


class DishAdmin(admin.ModelAdmin):
    """Admin configuration for Dish."""

    verbose_name_plural = "Dish"
    list_display = ('name', 'category', 'restaurant', 'created_at', 'updated_at')
    search_fields = ('name', 'category', 'restaurant')

    list_filter = ('category', 'restaurant')


admin.site.register(Dish, DishAdmin)
