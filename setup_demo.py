#!/usr/bin/env python
"""
Quick script to set up demo user on Railway
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waste_management.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_demo_user():
    """Create demo user if it doesn't exist"""
    email = 'demo@wastemanagement.com'
    password = 'demo123'
    
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': 'demo_user',
            'first_name': 'Demo',
            'last_name': 'User',
            'user_type': 'resident',
            'points': 1250,
            'level': 8,
            'recycling_streak': 15,
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'address': '123 Sample Street'
        }
    )
    
    if created:
        user.set_password(password)
        user.save()
        print(f"✅ Created demo user: {email}")
    else:
        # Update password in case it was changed
        user.set_password(password)
        user.save()
        print(f"✅ Updated demo user: {email}")
    
    print(f"📧 Email: {email}")
    print(f"🔑 Password: {password}")

if __name__ == '__main__':
    create_demo_user() 