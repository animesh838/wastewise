from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Badge, Leaderboard, Reward, UserReward, UserBadge

class GamificationHomeView(TemplateView):
    template_name = 'gamification/home.html'

class LeaderboardView(ListView):
    model = Leaderboard
    template_name = 'gamification/leaderboard.html'
    context_object_name = 'leaderboards'

class LeaderboardDetailView(DetailView):
    model = Leaderboard
    template_name = 'gamification/leaderboard_detail.html'
    context_object_name = 'leaderboard'
    slug_field = 'leaderboard_type'
    slug_url_kwarg = 'board_type'

class BadgeListView(ListView):
    model = Badge
    template_name = 'gamification/badges.html'
    context_object_name = 'badges'

class RewardListView(ListView):
    model = Reward
    template_name = 'gamification/rewards.html'
    context_object_name = 'rewards'
    
    def get_queryset(self):
        return Reward.objects.filter(is_active=True).order_by('points_cost')

class RedeemRewardView(LoginRequiredMixin, TemplateView):
    template_name = 'gamification/redeem_reward.html'

class MyRewardsView(LoginRequiredMixin, ListView):
    model = UserReward
    template_name = 'gamification/my_rewards.html'
    context_object_name = 'user_rewards'
    
    def get_queryset(self):
        return UserReward.objects.filter(user=self.request.user).order_by('-redeemed_at')

class AchievementView(LoginRequiredMixin, TemplateView):
    template_name = 'gamification/achievements.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_badges'] = UserBadge.objects.filter(user=user).order_by('-earned_at')
        return context
