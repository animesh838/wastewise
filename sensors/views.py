from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Bin, Sensor, Alert, SensorReading, MaintenanceLog

class SensorDashboardView(TemplateView):
    template_name = 'sensors/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_bins'] = Bin.objects.filter(is_active=True).count()
        context['active_alerts'] = Alert.objects.filter(is_resolved=False).count()
        context['bins_needing_collection'] = Bin.objects.filter(is_active=True).count()  # Placeholder
        return context

class BinListView(ListView):
    model = Bin
    template_name = 'sensors/bin_list.html'
    context_object_name = 'bins'

class BinDetailView(DetailView):
    model = Bin
    template_name = 'sensors/bin_detail.html'
    context_object_name = 'bin'

class AlertListView(ListView):
    model = Alert
    template_name = 'sensors/alerts.html'
    context_object_name = 'alerts'
    
    def get_queryset(self):
        return Alert.objects.filter(is_resolved=False).order_by('-created_at')

class ResolveAlertView(TemplateView):
    template_name = 'sensors/resolve_alert.html'

class MaintenanceLogView(ListView):
    model = MaintenanceLog
    template_name = 'sensors/maintenance.html'
    context_object_name = 'logs'

class SensorDataView(TemplateView):
    template_name = 'sensors/sensor_data.html'
