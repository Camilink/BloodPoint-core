#!/usr/bin/env python
"""
Test script for the achievement system
This can be run once the migration is applied to test the achievement functionality
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodpoint_project.settings')

try:
    django.setup()
    
    from bloodpoint_app.models import AchievementDefinition, donante, UserAchievement, UserStats
    from bloodpoint_app.services import AchievementService
    
    def test_achievement_system():
        print("🧪 Testing Achievement System")
        print("="*50)
        
        # Check if achievement definitions exist
        achievement_count = AchievementDefinition.objects.count()
        print(f"✅ Found {achievement_count} achievement definitions")
        
        if achievement_count == 0:
            print("❌ No achievements found. Running initialization...")
            AchievementService.initialize_achievements()
            achievement_count = AchievementDefinition.objects.count()
            print(f"✅ Created {achievement_count} achievement definitions")
        
        # Show achievement categories
        categories = AchievementDefinition.objects.values_list('category', flat=True).distinct()
        print(f"📂 Categories: {list(categories)}")
        
        # Show achievements by category
        for category in categories:
            achievements = AchievementDefinition.objects.filter(category=category)
            print(f"\n{category.upper()} Achievements:")
            for achievement in achievements:
                symbol = achievement.symbol or "🏆"
                print(f"  {symbol} {achievement.name} (req: {achievement.required_value})")
        
        # Test with existing donantes
        donantes = donante.objects.all()[:3]  # Test with first 3 donors
        
        print(f"\n🧑‍⚕️ Testing with {len(donantes)} donors:")
        for donante_obj in donantes:
            print(f"\nTesting donor: {donante_obj.nombre_completo}")
            
            # Check achievements
            new_achievements = AchievementService.check_and_award_achievements(donante_obj)
            
            # Get stats
            stats = AchievementService.get_or_create_user_stats(donante_obj)
            print(f"  Stats: {stats.total_donations} donations, {stats.different_centers} centers")
            
            # Get achievements
            user_achievements = AchievementService.get_user_achievements(donante_obj)
            print(f"  Achievements: {user_achievements.count()}")
            
            if new_achievements:
                print(f"  🎉 New achievements earned: {[a.name for a in new_achievements]}")
        
        print("\n✅ Achievement system test completed!")
        return True
        
    if __name__ == "__main__":
        test_achievement_system()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure Django is properly configured and migrations are applied")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
