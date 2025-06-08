from django.contrib import admin

from .models import Restaurant


class RestaurantAdmin(admin.ModelAdmin):
    """Admin configuration for Restaurant."""

    verbose_name_plural = "Restaurant"
    list_display = ('name', 'owner', 'created_at', 'updated_at')
    search_fields = ('name', 'owner')

    list_filter = ('owner',)


admin.site.register(Restaurant, RestaurantAdmin)
