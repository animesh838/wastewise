from django.contrib import admin
from .models import SensorType, Bin, Sensor, SensorReading, Alert, MaintenanceLog

@admin.register(SensorType)
class SensorTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'min_value', 'max_value']
    search_fields = ['name', 'description']

@admin.register(Bin)
class BinAdmin(admin.ModelAdmin):
    list_display = ['bin_id', 'location', 'waste_category', 'bin_size', 'capacity_liters', 'is_active', 'current_fill_level']
    list_filter = ['bin_size', 'waste_category', 'is_active', 'location__city']
    search_fields = ['bin_id', 'location__name', 'qr_code']
    readonly_fields = ['created_at', 'updated_at', 'current_fill_level']
    
    fieldsets = [
        (None, {
            'fields': ('bin_id', 'location', 'waste_category', 'is_active')
        }),
        ('Specifications', {
            'fields': ('bin_size', 'capacity_liters', 'qr_code')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Maintenance', {
            'fields': ('last_emptied', 'maintenance_due')
        }),
        ('Status', {
            'fields': ('current_fill_level',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    ]
    
    def current_fill_level(self, obj):
        return f"{obj.current_fill_level}%"
    current_fill_level.short_description = 'Fill Level'

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['sensor_id', 'bin', 'sensor_type', 'battery_level', 'is_active', 'needs_maintenance']
    list_filter = ['sensor_type', 'is_active', 'manufacturer', 'bin__location__city']
    search_fields = ['sensor_id', 'bin__bin_id', 'manufacturer', 'model']
    readonly_fields = ['created_at', 'updated_at', 'needs_maintenance']
    
    def needs_maintenance(self, obj):
        return obj.needs_maintenance
    needs_maintenance.boolean = True
    needs_maintenance.short_description = 'Needs Maintenance'

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'value', 'timestamp', 'is_anomaly']
    list_filter = ['is_anomaly', 'timestamp', 'sensor__sensor_type']
    search_fields = ['sensor__sensor_id', 'sensor__bin__bin_id']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('sensor__bin', 'sensor__sensor_type')

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['bin', 'alert_type', 'severity', 'is_resolved', 'created_at']
    list_filter = ['alert_type', 'severity', 'is_resolved', 'created_at']
    search_fields = ['bin__bin_id', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = [
        (None, {
            'fields': ('bin', 'sensor', 'alert_type', 'severity')
        }),
        ('Details', {
            'fields': ('message',)
        }),
        ('Resolution', {
            'fields': ('is_resolved', 'resolved_by', 'resolved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    ]

@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ['bin', 'maintenance_type', 'technician', 'cost', 'duration_minutes', 'created_at']
    list_filter = ['maintenance_type', 'created_at', 'bin__location__city']
    search_fields = ['bin__bin_id', 'technician__email', 'description']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = [
        (None, {
            'fields': ('bin', 'sensor', 'technician', 'maintenance_type')
        }),
        ('Details', {
            'fields': ('description', 'parts_used', 'cost', 'duration_minutes')
        }),
        ('Documentation', {
            'fields': ('before_photos', 'after_photos')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    ]
