from django.db.models.signals import post_save
from django.dispatch import receiver
from bookings.models import Booking, BookingData

@receiver(post_save, sender=Booking)

def create_booking_data(sender, instance, created, **kwargs):
## **kwargs are required to prevent "ValueError: Signal receivers must accept keyword arguments (**kwargs)."
    if created and not BookingData.objects.filter(booking=instance).exists():
        BookingData.objects.create(
            booking=instance,
            booking_status='confirmed',
        )