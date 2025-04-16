from django.urls import path
from .views import booking_view, success_view, user_bookings

urlpatterns = [
    path('book/', booking_view, name='booking_view'),
    path('success/', success_view, name='success'),
    path("my-bookings/", user_bookings, name="user_bookings"),
]