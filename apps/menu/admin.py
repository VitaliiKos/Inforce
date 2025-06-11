from django.contrib import admin
from .models import DailyMenu


@admin.register(DailyMenu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'date', 'dishes_count', 'created_at')
    list_filter = ('date', 'restaurant', 'created_at')
    search_fields = ('restaurant__name',)
    filter_horizontal = ('dishes',)
    date_hierarchy = 'date'

    def dishes_count(self, obj):
        return obj.dishes.count()

    dishes_count.short_description = 'Кількість страв'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('restaurant').prefetch_related('dishes')