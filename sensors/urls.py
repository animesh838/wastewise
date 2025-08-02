from django.urls import path
from . import views

app_name = 'sensors'

urlpatterns = [
    path('', views.SensorDashboardView.as_view(), name='dashboard'),
    path('bins/', views.BinListView.as_view(), name='bin_list'),
    path('bins/<int:pk>/', views.BinDetailView.as_view(), name='bin_detail'),
    path('alerts/', views.AlertListView.as_view(), name='alerts'),
    path('alerts/<int:pk>/resolve/', views.ResolveAlertView.as_view(), name='resolve_alert'),
    path('maintenance/', views.MaintenanceLogView.as_view(), name='maintenance'),
    path('data/', views.SensorDataView.as_view(), name='sensor_data'),
]