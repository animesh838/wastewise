from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    """
    Extended User model with profile information for waste management system
    """
    USER_TYPES = (
        ('resident', 'Resident'),
        ('collector', 'Waste Collector'),
        ('admin', 'Admin'),
    )
    
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='resident')
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Gamification fields
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    recycling_streak = models.IntegerField(default=0)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def add_points(self, points):
        """Add points and calculate level"""
        self.points += points
        # Simple level calculation: every 100 points = 1 level
        self.level = (self.points // 100) + 1
        self.save()
    
    class Meta:
        db_table = 'users'
