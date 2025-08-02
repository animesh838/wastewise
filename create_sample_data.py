#!/usr/bin/env python
"""
Script to create sample data for the WasteWise platform
Run this after setting up the database to populate with demo data
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waste_management.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from waste.models import WasteCategory, Location, WastePickupSchedule, WasteType
from sensors.models import SensorType, Bin, Sensor, SensorReading, Alert
from gamification.models import Badge, Reward, Leaderboard

User = get_user_model()

def create_sample_data():
    print("Creating sample data for WasteWise platform...")
    
    # Create waste categories
    print("Creating waste categories...")
    categories_data = [
        {'name': 'organic', 'description': 'Biodegradable food and garden waste', 'icon': 'bi-leaf'},
        {'name': 'plastic', 'description': 'Plastic bottles, containers, and packaging', 'icon': 'bi-cup-straw'},
        {'name': 'paper', 'description': 'Newspapers, cardboard, and office paper', 'icon': 'bi-file-earmark'},
        {'name': 'metal', 'description': 'Aluminum cans, steel items, and metal containers', 'icon': 'bi-gear'},
        {'name': 'glass', 'description': 'Glass bottles, jars, and containers', 'icon': 'bi-square'},
        {'name': 'electronic', 'description': 'Electronic devices, batteries, and e-waste', 'icon': 'bi-cpu'},
        {'name': 'hazardous', 'description': 'Chemical waste and hazardous materials', 'icon': 'bi-exclamation-triangle'},
        {'name': 'other', 'description': 'Other non-categorized waste', 'icon': 'bi-question-circle'},
    ]
    
    for cat_data in categories_data:
        category, created = WasteCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'icon': cat_data['icon'],
                'disposal_instructions': f"Proper disposal instructions for {cat_data['name']} waste."
            }
        )
        if created:
            print(f"Created category: {category.get_name_display()}")
    
    # Create locations
    print("Creating pickup locations...")
    locations_data = [
        {
            'name': 'Downtown Collection Center',
            'address': '123 Main Street',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'postal_code': '400001',
            'latitude': Decimal('19.0760'),
            'longitude': Decimal('72.8777')
        },
        {
            'name': 'North Side Hub',
            'address': '456 Oak Avenue',
            'city': 'Mumbai',
            'state': 'Maharashtra', 
            'postal_code': '400002',
            'latitude': Decimal('19.0896'),
            'longitude': Decimal('72.8656')
        },
        {
            'name': 'South End Station',
            'address': '789 Pine Road',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'postal_code': '400003',
            'latitude': Decimal('19.0544'),
            'longitude': Decimal('72.8322')
        },
        {
            'name': 'West Side Depot',
            'address': '321 Elm Street',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'postal_code': '400004',
            'latitude': Decimal('19.0330'),
            'longitude': Decimal('72.8697')
        }
    ]
    
    for loc_data in locations_data:
        location, created = Location.objects.get_or_create(
            name=loc_data['name'],
            defaults=loc_data
        )
        if created:
            print(f"Created location: {location.name}")
    
    # Create sample users
    print("Creating sample users...")
    users_data = [
        {
            'username': 'demo_user',
            'email': 'demo@wastemanagement.com',
            'first_name': 'Demo',
            'last_name': 'User',
            'user_type': 'resident',
            'points': 1250,
            'level': 8,
            'recycling_streak': 15
        },
        {
            'username': 'eco_warrior',
            'email': 'eco@wastemanagement.com',
            'first_name': 'Eco',
            'last_name': 'Warrior',
            'user_type': 'resident',
            'points': 2180,
            'level': 10,
            'recycling_streak': 25
        },
        {
            'username': 'collector_sam',
            'email': 'sam@wastemanagement.com',
            'first_name': 'Sam',
            'last_name': 'Collector',
            'user_type': 'collector',
            'points': 890,
            'level': 5,
            'recycling_streak': 8
        }
    ]
    
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'user_type': user_data['user_type'],
                'points': user_data['points'],
                'level': user_data['level'],
                'recycling_streak': user_data['recycling_streak'],
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'address': '123 Sample Street'
            }
        )
        if created:
            user.set_password('demo123')
            user.save()
            print(f"Created user: {user.username}")
    
    # Create sensor types
    print("Creating sensor types...")
    sensor_types_data = [
        {'name': 'fill_level', 'description': 'Ultrasonic fill level sensor', 'unit': '%', 'min_value': 0, 'max_value': 100},
        {'name': 'weight', 'description': 'Load cell weight sensor', 'unit': 'kg', 'min_value': 0, 'max_value': 500},
        {'name': 'temperature', 'description': 'Temperature sensor', 'unit': '°C', 'min_value': -10, 'max_value': 60},
        {'name': 'gas', 'description': 'Gas detection sensor', 'unit': 'ppm', 'min_value': 0, 'max_value': 1000},
    ]
    
    for sensor_data in sensor_types_data:
        sensor_type, created = SensorType.objects.get_or_create(
            name=sensor_data['name'],
            defaults=sensor_data
        )
        if created:
            print(f"Created sensor type: {sensor_type.get_name_display()}")
    
    # Create smart bins
    print("Creating smart bins...")
    locations = Location.objects.all()
    categories = WasteCategory.objects.all()
    
    bins_data = [
        {'bin_id': 'BIN-001', 'bin_size': 'large', 'capacity_liters': 240},
        {'bin_id': 'BIN-002', 'bin_size': 'medium', 'capacity_liters': 120},
        {'bin_id': 'BIN-003', 'bin_size': 'medium', 'capacity_liters': 120},
        {'bin_id': 'BIN-004', 'bin_size': 'small', 'capacity_liters': 50},
    ]
    
    for i, bin_data in enumerate(bins_data):
        location = locations[i % len(locations)]
        category = categories[i % len(categories)]
        
        bin_obj, created = Bin.objects.get_or_create(
            bin_id=bin_data['bin_id'],
            defaults={
                'location': location,
                'waste_category': category,
                'bin_size': bin_data['bin_size'],
                'capacity_liters': bin_data['capacity_liters'],
                'latitude': location.latitude,
                'longitude': location.longitude,
                'qr_code': f"QR-{bin_data['bin_id']}"
            }
        )
        if created:
            print(f"Created bin: {bin_obj.bin_id}")
    
    # Create badges
    print("Creating badges...")
    badges_data = [
        {
            'name': 'Eco Warrior',
            'description': 'Complete your first 10 waste pickups',
            'badge_type': 'recycling',
            'points_required': 100,
            'rarity': 'common'
        },
        {
            'name': 'Streak Master',
            'description': 'Maintain a 7-day recycling streak',
            'badge_type': 'consistency',
            'points_required': 200,
            'rarity': 'rare'
        },
        {
            'name': 'Community Hero',
            'description': 'Help 50 community members with recycling',
            'badge_type': 'community',
            'points_required': 500,
            'rarity': 'epic'
        },
        {
            'name': 'Rising Star',
            'description': 'Reach level 5 in the first month',
            'badge_type': 'milestone',
            'points_required': 300,
            'rarity': 'rare'
        }
    ]
    
    for badge_data in badges_data:
        badge, created = Badge.objects.get_or_create(
            name=badge_data['name'],
            defaults=badge_data
        )
        if created:
            print(f"Created badge: {badge.name}")
    
    # Create rewards
    print("Creating rewards...")
    rewards_data = [
        {
            'name': 'Coffee Shop Voucher',
            'description': '$5 off your next coffee purchase',
            'reward_type': 'voucher',
            'points_cost': 500,
            'monetary_value': Decimal('5.00'),
            'stock_quantity': 20
        },
        {
            'name': 'Plant a Tree',
            'description': 'Donate to plant a tree in your name',
            'reward_type': 'donation',
            'points_cost': 1000,
            'monetary_value': Decimal('10.00'),
            'stock_quantity': None
        },
        {
            'name': 'Bike Rental Credit',
            'description': '2 hours free bike rental',
            'reward_type': 'service',
            'points_cost': 750,
            'monetary_value': Decimal('15.00'),
            'stock_quantity': 15
        }
    ]
    
    for reward_data in rewards_data:
        reward, created = Reward.objects.get_or_create(
            name=reward_data['name'],
            defaults=reward_data
        )
        if created:
            print(f"Created reward: {reward.name}")
    
    # Create leaderboards
    print("Creating leaderboards...")
    leaderboards_data = [
        {
            'name': 'Weekly Points Leaders',
            'leaderboard_type': 'points_weekly',
            'timeframe': 'weekly',
            'description': 'Top point earners this week'
        },
        {
            'name': 'Monthly Champions',
            'leaderboard_type': 'points_monthly',
            'timeframe': 'monthly',
            'description': 'Monthly leaderboard champions'
        },
        {
            'name': 'All-Time Heroes',
            'leaderboard_type': 'points_all_time',
            'timeframe': 'all_time',
            'description': 'All-time point leaders'
        }
    ]
    
    for leaderboard_data in leaderboards_data:
        leaderboard, created = Leaderboard.objects.get_or_create(
            name=leaderboard_data['name'],
            defaults=leaderboard_data
        )
        if created:
            print(f"Created leaderboard: {leaderboard.name}")
    
    print("\n✅ Sample data creation completed successfully!")
    print("\nDemo login credentials:")
    print("Username: demo_user")
    print("Password: demo123")
    print("\nAdmin access:")
    print("Visit /admin/ and use the superuser account you created")

if __name__ == '__main__':
    create_sample_data()