from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class WasteType(models.Model):
    """Different types of waste that can be collected"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color_code = models.CharField(max_length=7, default='#000000', help_text='Hex color code for UI')
    is_recyclable = models.BooleanField(default=True)
    points_per_kg = models.IntegerField(default=10, help_text='Points awarded per kg of this waste type')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class WasteCategory(models.Model):
    """Categories for waste segregation"""
    CATEGORY_CHOICES = [
        ('organic', 'Organic/Biodegradable'),
        ('plastic', 'Plastic'),
        ('paper', 'Paper'),
        ('metal', 'Metal'),
        ('glass', 'Glass'),
        ('electronic', 'Electronic Waste'),
        ('hazardous', 'Hazardous'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='CSS icon class')
    disposal_instructions = models.TextField(blank=True)
    
    def __str__(self):
        return self.get_name_display()
    
    class Meta:
        verbose_name_plural = 'Waste Categories'

class Location(models.Model):
    """Locations for waste collection"""
    name = models.CharField(max_length=200)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.city}"
    
    class Meta:
        ordering = ['city', 'name']

class WastePickupSchedule(models.Model):
    """Schedule for waste pickup"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pickup_schedules')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    waste_category = models.ForeignKey(WasteCategory, on_delete=models.CASCADE)
    estimated_weight = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.1)])
    actual_weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    special_instructions = models.TextField(blank=True)
    assigned_collector = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_pickups',
        limit_choices_to={'user_type': 'collector'}
    )
    pickup_photo = models.ImageField(upload_to='pickup_photos/', blank=True, null=True)
    notes = models.TextField(blank=True)
    points_awarded = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Pickup - {self.user.email} - {self.scheduled_date}"
    
    def calculate_points(self):
        """Calculate points based on actual weight and waste type"""
        if self.actual_weight and self.waste_category:
            # Base points calculation
            base_points = int(self.actual_weight * 10)  # 10 points per kg
            
            # Bonus for proper segregation
            segregation_bonus = base_points * 0.2 if self.status == 'completed' else 0
            
            # Priority bonus
            priority_multiplier = {
                'low': 1.0,
                'medium': 1.1,
                'high': 1.2,
                'urgent': 1.5
            }
            
            total_points = int((base_points + segregation_bonus) * priority_multiplier.get(self.priority, 1.0))
            return total_points
        return 0
    
    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.points_awarded:
            self.points_awarded = self.calculate_points()
            if self.points_awarded > 0:
                self.user.add_points(self.points_awarded)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-scheduled_date', '-scheduled_time']

class WasteCollection(models.Model):
    """Record of actual waste collection"""
    pickup_schedule = models.OneToOneField(WastePickupSchedule, on_delete=models.CASCADE)
    collector = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    collection_date = models.DateTimeField(auto_now_add=True)
    actual_weight = models.DecimalField(max_digits=8, decimal_places=2)
    quality_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Quality of waste segregation (1-5)'
    )
    recycled_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Percentage of waste that was recyclable'
    )
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Collection - {self.pickup_schedule.user.email} - {self.collection_date.date()}"
    
    class Meta:
        ordering = ['-collection_date']
