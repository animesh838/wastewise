from django.urls import path
from . import views

app_name = 'waste'

urlpatterns = [
    path('', views.WasteHomeView.as_view(), name='home'),
    path('schedule/', views.SchedulePickupView.as_view(), name='schedule_pickup'),
    path('schedule/<int:pk>/', views.PickupDetailView.as_view(), name='pickup_detail'),
    path('schedule/<int:pk>/edit/', views.PickupEditView.as_view(), name='pickup_edit'),
    path('schedule/<int:pk>/cancel/', views.PickupCancelView.as_view(), name='pickup_cancel'),
    path('my-schedules/', views.MySchedulesView.as_view(), name='my_schedules'),
    path('locations/', views.LocationListView.as_view(), name='locations'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('history/', views.CollectionHistoryView.as_view(), name='history'),
]