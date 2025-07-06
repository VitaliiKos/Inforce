from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from apps.employee.models import Employee, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fk_name = 'user'
    extra = 0
    fields = ('first_name', 'last_name', 'phone', 'avatar_preview', 'avatar', 'created_at', 'updated_at')
    readonly_fields = ('avatar_preview', 'created_at', 'updated_at')

    def avatar_preview(self, instance):
        if instance.avatar:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit: cover; border-radius: 50%;" />',
                instance.avatar.url
            )
        return "-"

    avatar_preview.short_description = "Avatar Preview"


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('email', 'is_staff', 'is_active', 'last_login')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('email', 'last_login', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('email',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'created_at', 'updated_at'),
        }),
    )


    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile')

    def get_phone(self, obj):
        return obj.profile.phone if hasattr(obj, 'profile') else '-'

    get_phone.short_description = 'Phone'
