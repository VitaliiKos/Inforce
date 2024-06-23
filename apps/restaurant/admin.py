from django.contrib import admin

from .models import Menu, Restaurant, Vote


class RestaurantAdmin(admin.ModelAdmin):
    """Admin configuration for Restaurant."""

    verbose_name_plural = "Restaurant"
    list_display = ('name', 'owner', 'created_at', 'updated_at')
    search_fields = ('name', 'owner')

    list_filter = ('owner',)


class MenuAdmin(admin.ModelAdmin):
    """Admin configuration for Menu."""

    verbose_name_plural = "Menu"
    list_display = ('dish', 'restaurant', 'date')
    search_fields = ('dish',)

    list_filter = ('restaurant', 'date')


class VoteAdmin(admin.ModelAdmin):
    """Admin configuration for Vote."""

    verbose_name_plural = "Vote"
    list_display = ('menu', 'employee')

    list_filter = ('menu',)


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Vote, VoteAdmin)
