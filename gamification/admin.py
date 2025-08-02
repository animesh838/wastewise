from django.contrib import admin
from .models import Badge, UserBadge, Leaderboard, Reward, UserReward

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'badge_type', 'rarity', 'points_required', 'is_active', 'earned_count']
    list_filter = ['badge_type', 'rarity', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'earned_count']
    
    def earned_count(self, obj):
        return obj.earned_count()
    earned_count.short_description = 'Times Earned'

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at', 'progress']
    list_filter = ['badge__badge_type', 'badge__rarity', 'earned_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'badge__name']
    readonly_fields = ['earned_at']
    date_hierarchy = 'earned_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'badge')

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['name', 'leaderboard_type', 'timeframe', 'is_active', 'last_updated']
    list_filter = ['leaderboard_type', 'timeframe', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['last_updated']

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ['name', 'reward_type', 'points_cost', 'monetary_value', 'stock_quantity', 'is_active', 'is_available']
    list_filter = ['reward_type', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'partner_company']
    readonly_fields = ['created_at', 'is_available']
    
    fieldsets = [
        (None, {
            'fields': ('name', 'description', 'reward_type', 'is_active')
        }),
        ('Cost & Value', {
            'fields': ('points_cost', 'monetary_value', 'stock_quantity')
        }),
        ('Partner Info', {
            'fields': ('partner_company',)
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Availability', {
            'fields': ('is_available',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    ]
    
    def is_available(self, obj):
        return obj.is_available
    is_available.boolean = True
    is_available.short_description = 'Available'

@admin.register(UserReward)
class UserRewardAdmin(admin.ModelAdmin):
    list_display = ['user', 'reward', 'status', 'redemption_code', 'points_spent', 'redeemed_at']
    list_filter = ['status', 'reward__reward_type', 'redeemed_at']
    search_fields = ['user__email', 'reward__name', 'redemption_code']
    readonly_fields = ['redeemed_at', 'redemption_code']
    date_hierarchy = 'redeemed_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'reward')
