from django.urls import path
from .views import staff_panel_view
from . import views

app_name = "staffpanel"

urlpatterns = [
    path('staff/', staff_panel_view, name='staff_panel'),
    path('mark_completed/<int:booking_id>/', views.mark_completed, name='mark_completed'),
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('deleted-log/', views.deleted_bookings_log, name='deleted_log'),
    path('edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    ###
    path('analytics/', views.analytics_view, name='staff_analytics'),
]
