from django.urls import path
from . import views

app_name = 'gamification'

urlpatterns = [
    path('', views.GamificationHomeView.as_view(), name='home'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('leaderboard/<str:board_type>/', views.LeaderboardDetailView.as_view(), name='leaderboard_detail'),
    path('badges/', views.BadgeListView.as_view(), name='badges'),
    path('rewards/', views.RewardListView.as_view(), name='rewards'),
    path('rewards/<int:pk>/redeem/', views.RedeemRewardView.as_view(), name='redeem_reward'),
    path('my-rewards/', views.MyRewardsView.as_view(), name='my_rewards'),
    path('achievements/', views.AchievementView.as_view(), name='achievements'),
]