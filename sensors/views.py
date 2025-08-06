from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from .models import Bin, Sensor, Alert, SensorReading, MaintenanceLog

def is_admin_or_collector(user):
    """Check if user is admin or collector"""
    return user.is_superuser or user.user_type in ['admin', 'collector']

class SensorDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'sensors/dashboard.html'
    
    def test_func(self):
        """Only allow superusers, admins, and collectors"""
        return is_admin_or_collector(self.request.user)
    
    def handle_no_permission(self):
        """Redirect to home with error message"""
        return HttpResponseForbidden(
            "<h1>Access Denied</h1><p>You don't have permission to view the sensor dashboard. "
            "This feature is restricted to administrators and waste collectors.</p>"
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_bins'] = Bin.objects.filter(is_active=True).count()
        context['active_alerts'] = Alert.objects.filter(is_resolved=False).count()
        context['bins_needing_collection'] = Bin.objects.filter(is_active=True).count()  # Placeholder
        return context

class BinListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Bin
    template_name = 'sensors/bin_list.html'
    context_object_name = 'bins'
    
    def test_func(self):
        return is_admin_or_collector(self.request.user)

class BinDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Bin
    template_name = 'sensors/bin_detail.html'
    context_object_name = 'bin'
    
    def test_func(self):
        return is_admin_or_collector(self.request.user)

class AlertListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Alert
    template_name = 'sensors/alerts.html'
    context_object_name = 'alerts'
    
    def test_func(self):
        return is_admin_or_collector(self.request.user)
    
    def get_queryset(self):
        return Alert.objects.filter(is_resolved=False).order_by('-created_at')

class ResolveAlertView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'sensors/resolve_alert.html'
    
    def test_func(self):
        return is_admin_or_collector(self.request.user)

class MaintenanceLogView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = MaintenanceLog
    template_name = 'sensors/maintenance.html'
    context_object_name = 'logs'
    
    def test_func(self):
        return is_admin_or_collector(self.request.user)

class SensorDataView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'sensors/sensor_data.html'
    
    def test_func(self):
        return is_admin_or_collector(self.request.user)
