from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse_lazy

class RegisterView(TemplateView):
    template_name = 'users/register.html'

class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

class LogoutView(View):
    template_name = 'users/logout.html'
    
    def get(self, request):
        # Show logout confirmation page
        return render(request, self.template_name)
    
    def post(self, request):
        # Actually logout the user
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('home')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

class ProfileEditView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile_edit.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get user's pickup schedules
        context['total_pickups'] = user.pickup_schedules.filter(status='completed').count()
        context['pending_pickups'] = user.pickup_schedules.filter(status='pending').count()
        context['recent_pickups'] = user.pickup_schedules.order_by('-created_at')[:5]
        
        return context
