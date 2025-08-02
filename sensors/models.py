from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from waste.models import Location, WasteCategory

User = get_user_model()

class SensorType(models.Model):
    """Types of sensors available"""
    SENSOR_TYPES = [
        ('fill_level', 'Fill Level Sensor'),
        ('weight', 'Weight Sensor'),
        ('temperature', 'Temperature Sensor'),
        ('humidity', 'Humidity Sensor'),
        ('gas', 'Gas Detection Sensor'),
        ('motion', 'Motion Sensor'),
    ]
    
    name = models.CharField(max_length=50, choices=SENSOR_TYPES, unique=True)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=20, help_text='Measurement unit (e.g., %, kg, °C)')
    min_value = models.FloatField(default=0)
    max_value = models.FloatField(default=100)
    
    def __str__(self):
        return self.get_name_display()

class Bin(models.Model):
    """Smart waste bins with sensors"""
    BIN_SIZES = [
        ('small', 'Small (50L)'),
        ('medium', 'Medium (120L)'),
        ('large', 'Large (240L)'),
        ('industrial', 'Industrial (1000L+)'),
    ]
    
    bin_id = models.CharField(max_length=50, unique=True, help_text='Unique bin identifier')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='bins')
    waste_category = models.ForeignKey(WasteCategory, on_delete=models.CASCADE)
    bin_size = models.CharField(max_length=20, choices=BIN_SIZES, default='medium')
    capacity_liters = models.IntegerField(help_text='Bin capacity in liters')
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_emptied = models.DateTimeField(null=True, blank=True)
    maintenance_due = models.DateField(null=True, blank=True)
    qr_code = models.CharField(max_length=200, blank=True, help_text='QR code for bin identification')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Bin {self.bin_id} - {self.location.name}"
    
    @property
    def current_fill_level(self):
        """Get the most recent fill level reading"""
        latest_reading = self.sensor_readings.filter(
            sensor__sensor_type__name='fill_level'
        ).order_by('-timestamp').first()
        return latest_reading.value if latest_reading else 0
    
    @property
    def is_full(self):
        """Check if bin is considered full (>80%)"""
        return self.current_fill_level > 80
    
    @property
    def needs_collection(self):
        """Check if bin needs collection (>70%)"""
        return self.current_fill_level > 70
    
    class Meta:
        ordering = ['bin_id']

class Sensor(models.Model):
    """Individual sensors attached to bins"""
    sensor_id = models.CharField(max_length=50, unique=True)
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE, related_name='sensors')
    sensor_type = models.ForeignKey(SensorType, on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    firmware_version = models.CharField(max_length=50, blank=True)
    battery_level = models.IntegerField(
        default=100, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Battery level percentage'
    )
    calibration_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.sensor_id} - {self.sensor_type.name} - {self.bin.bin_id}"
    
    @property
    def needs_maintenance(self):
        """Check if sensor needs maintenance"""
        return self.battery_level < 20 or not self.is_active
    
    class Meta:
        ordering = ['sensor_id']

class SensorReading(models.Model):
    """Individual sensor readings/data points"""
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings')
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_anomaly = models.BooleanField(default=False, help_text='Flagged as unusual reading')
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.sensor.sensor_id} - {self.value} at {self.timestamp}"
    
    def save(self, *args, **kwargs):
        # Auto-detect anomalies based on sensor type limits
        sensor_type = self.sensor.sensor_type
        if self.value < sensor_type.min_value or self.value > sensor_type.max_value:
            self.is_anomaly = True
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['sensor', '-timestamp']),
            models.Index(fields=['-timestamp']),
        ]

class Alert(models.Model):
    """Alerts generated by sensor data"""
    ALERT_TYPES = [
        ('bin_full', 'Bin Full'),
        ('bin_overflow', 'Bin Overflow'),
        ('sensor_malfunction', 'Sensor Malfunction'),
        ('low_battery', 'Low Battery'),
        ('maintenance_due', 'Maintenance Due'),
        ('unusual_activity', 'Unusual Activity'),
    ]
    
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE, related_name='alerts')
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True, blank=True)
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS, default='medium')
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.bin.bin_id}"
    
    class Meta:
        ordering = ['-created_at']

class MaintenanceLog(models.Model):
    """Log of maintenance activities"""
    MAINTENANCE_TYPES = [
        ('cleaning', 'Cleaning'),
        ('repair', 'Repair'),
        ('calibration', 'Sensor Calibration'),
        ('battery_replacement', 'Battery Replacement'),
        ('software_update', 'Software Update'),
        ('inspection', 'Routine Inspection'),
    ]
    
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE, related_name='maintenance_logs')
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True, blank=True)
    technician = models.ForeignKey(User, on_delete=models.CASCADE)
    maintenance_type = models.CharField(max_length=30, choices=MAINTENANCE_TYPES)
    description = models.TextField()
    parts_used = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    before_photos = models.ImageField(upload_to='maintenance/before/', blank=True, null=True)
    after_photos = models.ImageField(upload_to='maintenance/after/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_maintenance_type_display()} - {self.bin.bin_id} - {self.created_at.date()}"
    
    class Meta:
        ordering = ['-created_at']
