from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import WastePickupSchedule, WasteCategory, Location, WasteCollection

class WasteHomeView(TemplateView):
    template_name = 'waste/home.html'

class SchedulePickupView(LoginRequiredMixin, TemplateView):
    template_name = 'waste/schedule_pickup.html'

class PickupDetailView(LoginRequiredMixin, DetailView):
    model = WastePickupSchedule
    template_name = 'waste/pickup_detail.html'
    context_object_name = 'pickup'

class PickupEditView(LoginRequiredMixin, TemplateView):
    template_name = 'waste/pickup_edit.html'

class PickupCancelView(LoginRequiredMixin, TemplateView):
    template_name = 'waste/pickup_cancel.html'

class MySchedulesView(LoginRequiredMixin, ListView):
    model = WastePickupSchedule
    template_name = 'waste/my_schedules.html'
    context_object_name = 'schedules'
    
    def get_queryset(self):
        return WastePickupSchedule.objects.filter(user=self.request.user).order_by('-created_at')

class LocationListView(ListView):
    model = Location
    template_name = 'waste/locations.html'
    context_object_name = 'locations'

class CategoryListView(ListView):
    model = WasteCategory
    template_name = 'waste/categories.html'
    context_object_name = 'categories'

class CollectionHistoryView(LoginRequiredMixin, ListView):
    model = WasteCollection
    template_name = 'waste/history.html'
    context_object_name = 'collections'
    
    def get_queryset(self):
        return WasteCollection.objects.filter(
            pickup_schedule__user=self.request.user
        ).order_by('-collection_date')
