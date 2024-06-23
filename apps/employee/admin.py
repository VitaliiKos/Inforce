from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Admin configuration for the UserModel."""

    list_display = ['first_name', 'last_name', 'email', 'is_staff', 'is_active', 'created_at', 'updated_at']
