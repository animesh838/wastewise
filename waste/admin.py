from django.contrib import admin
from .models import WasteType, WasteCategory, Location, WastePickupSchedule, WasteCollection

@admin.register(WasteType)
class WasteTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_recyclable', 'points_per_kg', 'created_at']
    list_filter = ['is_recyclable', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']

@admin.register(WasteCategory)
class WasteCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name', 'description']
    list_per_page = 20

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'postal_code', 'is_active', 'created_at']
    list_filter = ['city', 'state', 'is_active', 'created_at']
    search_fields = ['name', 'address', 'city', 'state']
    readonly_fields = ['created_at']
    fieldsets = [
        (None, {
            'fields': ('name', 'address', 'is_active')
        }),
        ('Location Details', {
            'fields': ('city', 'state', 'postal_code', 'latitude', 'longitude')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    ]

@admin.register(WastePickupSchedule)
class WastePickupScheduleAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'waste_category', 'scheduled_date', 'status', 'priority', 'points_awarded']
    list_filter = ['status', 'priority', 'waste_category', 'scheduled_date', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'location__name']
    readonly_fields = ['created_at', 'updated_at', 'points_awarded']
    date_hierarchy = 'scheduled_date'
    
    fieldsets = [
        (None, {
            'fields': ('user', 'location', 'waste_category', 'status', 'priority')
        }),
        ('Schedule Details', {
            'fields': ('scheduled_date', 'scheduled_time', 'estimated_weight', 'actual_weight')
        }),
        ('Assignment', {
            'fields': ('assigned_collector', 'special_instructions', 'notes')
        }),
        ('Media', {
            'fields': ('pickup_photo',)
        }),
        ('Points & Completion', {
            'fields': ('points_awarded', 'completed_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    ]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'location', 'waste_category', 'assigned_collector')

@admin.register(WasteCollection)
class WasteCollectionAdmin(admin.ModelAdmin):
    list_display = ['pickup_schedule', 'collector', 'collection_date', 'actual_weight', 'quality_rating', 'recycled_percentage']
    list_filter = ['quality_rating', 'collection_date', 'recycled_percentage']
    search_fields = ['pickup_schedule__user__email', 'collector__email']
    readonly_fields = ['collection_date']
    date_hierarchy = 'collection_date'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('pickup_schedule__user', 'collector')
