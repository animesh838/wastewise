from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import viewsets when they're created
# from users.api_views import UserViewSet
# from waste.api_views import WastePickupScheduleViewSet, LocationViewSet
# from sensors.api_views import BinViewSet, SensorReadingViewSet, AlertViewSet
# from gamification.api_views import LeaderboardViewSet, RewardViewSet

router = DefaultRouter()

# Register viewsets when they're created
# router.register(r'users', UserViewSet)
# router.register(r'pickups', WastePickupScheduleViewSet)
# router.register(r'locations', LocationViewSet)
# router.register(r'bins', BinViewSet)
# router.register(r'sensor-readings', SensorReadingViewSet)
# router.register(r'alerts', AlertViewSet)
# router.register(r'leaderboards', LeaderboardViewSet)
# router.register(r'rewards', RewardViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]