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

class BadgeListView(LoginRequiredMixin, ListView):
    model = Badge
    template_name = 'gamification/badges.html'
    context_object_name = 'badges'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get user's earned badges
        user_badges = UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
        context['user_badges'] = Badge.objects.filter(id__in=user_badges)
        
        # Calculate statistics
        context['total_points'] = sum(badge.points_required for badge in context['user_badges'])
        context['completion_percentage'] = int((len(context['user_badges']) / max(len(context['badges']), 1)) * 100)
        context['rare_badges'] = len(context['user_badges'].filter(rarity__in=['rare', 'epic', 'legendary']))
        
        return context

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
