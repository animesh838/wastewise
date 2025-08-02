from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin"""
    list_display = ['email', 'username', 'full_name', 'user_type', 'points', 'level', 'is_verified', 'is_active']
    list_filter = ['user_type', 'is_verified', 'is_active', 'city', 'state']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'phone_number']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Info', {
            'fields': ('phone_number', 'user_type', 'profile_picture', 'is_verified')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postal_code')
        }),
        ('Gamification', {
            'fields': ('points', 'level', 'recycling_streak')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Profile Info', {
            'fields': ('email', 'phone_number', 'user_type')
        }),
    )
