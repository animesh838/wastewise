from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Badge(models.Model):
    """Badges that users can earn"""
    BADGE_TYPES = [
        ('recycling', 'Recycling Achievement'),
        ('consistency', 'Consistency'),
        ('community', 'Community Participation'),
        ('milestone', 'Milestone'),
        ('special', 'Special Event'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES)
    icon = models.ImageField(upload_to='badges/', blank=True, null=True)
    icon_class = models.CharField(max_length=50, blank=True, help_text='CSS icon class as fallback')
    color = models.CharField(max_length=7, default='#4CAF50', help_text='Hex color code')
    points_required = models.IntegerField(default=0, help_text='Minimum points to earn this badge')
    is_active = models.BooleanField(default=True)
    rarity = models.CharField(
        max_length=10,
        choices=[('common', 'Common'), ('rare', 'Rare'), ('epic', 'Epic'), ('legendary', 'Legendary')],
        default='common'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def earned_count(self):
        """Number of users who have earned this badge"""
        return self.user_badges.count()
    
    class Meta:
        ordering = ['badge_type', 'points_required']

class UserBadge(models.Model):
    """Junction table for users and their earned badges"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='user_badges')
    earned_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=100, help_text='Progress percentage when earned')
    
    class Meta:
        unique_together = ['user', 'badge']
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.badge.name}"

class Leaderboard(models.Model):
    """Different types of leaderboards"""
    LEADERBOARD_TYPES = [
        ('points_weekly', 'Weekly Points'),
        ('points_monthly', 'Monthly Points'),
        ('points_all_time', 'All-Time Points'),
        ('recycling_streak', 'Longest Recycling Streak'),
        ('weight_recycled', 'Most Weight Recycled'),
    ]
    
    TIMEFRAMES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('all_time', 'All Time'),
    ]
    
    name = models.CharField(max_length=100)
    leaderboard_type = models.CharField(max_length=20, choices=LEADERBOARD_TYPES)
    timeframe = models.CharField(max_length=10, choices=TIMEFRAMES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_timeframe_display()})"
    
    class Meta:
        ordering = ['leaderboard_type', 'timeframe']

class Reward(models.Model):
    """Rewards that users can redeem with points"""
    REWARD_TYPES = [
        ('discount', 'Discount Coupon'),
        ('voucher', 'Gift Voucher'),
        ('merchandise', 'Merchandise'),
        ('service', 'Service Credit'),
        ('donation', 'Charity Donation'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    reward_type = models.CharField(max_length=20, choices=REWARD_TYPES)
    points_cost = models.IntegerField()
    monetary_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='rewards/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    stock_quantity = models.IntegerField(null=True, blank=True, help_text='Leave blank for unlimited')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.points_cost} points)"
    
    @property
    def is_available(self):
        """Check if reward is available for redemption"""
        if not self.is_active:
            return False
        if self.stock_quantity is not None and self.stock_quantity <= 0:
            return False
        return True
    
    class Meta:
        ordering = ['points_cost']

class UserReward(models.Model):
    """User's redeemed rewards"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('redeemed', 'Redeemed'),
        ('used', 'Used'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rewards')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='user_rewards')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    redemption_code = models.CharField(max_length=50, unique=True)
    redeemed_at = models.DateTimeField(auto_now_add=True)
    points_spent = models.IntegerField()
    
    def __str__(self):
        return f"{self.user.email} - {self.reward.name} - {self.redemption_code}"
    
    def save(self, *args, **kwargs):
        if not self.redemption_code:
            import uuid
            self.redemption_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-redeemed_at']
