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

def create_superuser():
    """Create superuser if it doesn't exist"""
    email = 'admin@wastemanagement.com'
    password = 'admin123'
    
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': 'admin_user',
            'first_name': 'Admin',
            'last_name': 'User',
            'user_type': 'admin',
            'is_superuser': True,
            'is_staff': True,
            'points': 5000,
            'level': 15,
            'recycling_streak': 30,
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'address': '456 Admin Street'
        }
    )
    
    if created:
        user.set_password(password)
        user.save()
        print(f"✅ Created superuser: {email}")
    else:
        # Update password in case it was changed
        user.set_password(password)
        user.save()
        print(f"✅ Updated superuser: {email}")
    
    print(f"📧 Admin Email: {email}")
    print(f"🔑 Admin Password: {password}")

if __name__ == '__main__':
    create_demo_user()
    create_superuser() 