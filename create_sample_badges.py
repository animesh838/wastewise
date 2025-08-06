#!/usr/bin/env python
"""
Script to create sample badges for the gamification system
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waste_management.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from gamification.models import Badge

def create_sample_badges():
    """Create sample badges"""
    
    badges_data = [
        {
            'name': 'Recycling Rookie',
            'description': 'Complete your first waste pickup. Schedule and complete 1 waste pickup to earn this badge.',
            'badge_type': 'recycling',
            'icon_class': 'bi-recycle',
            'color': '#28a745',
            'points_required': 50,
            'rarity': 'common'
        },
        {
            'name': 'Green Guardian',
            'description': 'Complete 10 waste pickups. Schedule and complete 10 waste pickups to earn this badge.',
            'badge_type': 'recycling',
            'icon_class': 'bi-shield-check',
            'color': '#007bff',
            'points_required': 100,
            'rarity': 'common'
        },
        {
            'name': 'Eco Warrior',
            'description': 'Complete 50 waste pickups. Schedule and complete 50 waste pickups to earn this badge.',
            'badge_type': 'recycling',
            'icon_class': 'bi-shield-star',
            'color': '#ffc107',
            'points_required': 250,
            'rarity': 'rare'
        },
        {
            'name': 'Sustainability Master',
            'description': 'Complete 100 waste pickups. Schedule and complete 100 waste pickups to earn this badge.',
            'badge_type': 'recycling',
            'icon_class': 'bi-trophy',
            'color': '#dc3545',
            'points_required': 500,
            'rarity': 'epic'
        },
        {
            'name': 'Waste Wizard',
            'description': 'Complete 500 waste pickups. Schedule and complete 500 waste pickups to earn this badge.',
            'badge_type': 'recycling',
            'icon_class': 'bi-magic',
            'color': '#17a2b8',
            'points_required': 1000,
            'rarity': 'legendary'
        },
        {
            'name': 'Streak Starter',
            'description': 'Maintain a 7-day recycling streak. Recycle for 7 consecutive days to earn this badge.',
            'badge_type': 'consistency',
            'icon_class': 'bi-fire',
            'color': '#ffc107',
            'points_required': 75,
            'rarity': 'common'
        },
        {
            'name': 'Streak Master',
            'description': 'Maintain a 30-day recycling streak. Recycle for 30 consecutive days to earn this badge.',
            'badge_type': 'consistency',
            'icon_class': 'bi-fire',
            'color': '#dc3545',
            'points_required': 300,
            'rarity': 'rare'
        },
        {
            'name': 'Community Hero',
            'description': 'Help 10 neighbors with waste management. Assist 10 different neighbors to earn this badge.',
            'badge_type': 'community',
            'icon_class': 'bi-people',
            'color': '#007bff',
            'points_required': 150,
            'rarity': 'rare'
        },
        {
            'name': 'Innovation Leader',
            'description': 'Suggest 5 improvements to the system. Submit 5 feedback suggestions to earn this badge.',
            'badge_type': 'community',
            'icon_class': 'bi-lightbulb',
            'color': '#ffc107',
            'points_required': 200,
            'rarity': 'epic'
        },
        {
            'name': 'Environmental Champion',
            'description': 'Achieve perfect waste segregation for 1 month. Perfect segregation for 30 days to earn this badge.',
            'badge_type': 'milestone',
            'icon_class': 'bi-award',
            'color': '#28a745',
            'points_required': 400,
            'rarity': 'legendary'
        }
    ]
    
    created_count = 0
    for badge_data in badges_data:
        badge, created = Badge.objects.get_or_create(
            name=badge_data['name'],
            defaults=badge_data
        )
        if created:
            created_count += 1
            print(f"✅ Created badge: {badge.name}")
        else:
            print(f"ℹ️  Badge already exists: {badge.name}")
    
    print(f"\n🎉 Created {created_count} new badges!")
    print(f"📊 Total badges in system: {Badge.objects.count()}")

if __name__ == '__main__':
    create_sample_badges() 