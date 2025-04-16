from django.db import models
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15) #setting as a charfield to account for country codes, will make sure regex checks number
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} ({self.email})"

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)  
    table_size = models.IntegerField()
    kids = models.BooleanField(default=False)
    time = models.CharField(max_length=10)  
    date = models.DateField()
    special_requests = models.TextField(blank=True, null=True) #textfield allows for longer length than charfield 

    completed = models.BooleanField(default=False) #for staff to flag tables as completed or no show
    def __str__(self):
        return f"{self.customer.name} - {self.date} at {self.time}"
    
#################
class BookingData(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  
    day_of_week = models.CharField(max_length=10)  
    booking_status = models.CharField(max_length=20) 
    booking_time = models.TimeField()  
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.created_at:
            self.created_at = timezone.now()

        if not self.day_of_week:
            self.day_of_week = self.created_at.strftime('%A')

        if not self.booking_time:
            self.booking_time = self.created_at.time()

    
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return f"BookingData for Booking ID: {self.booking.id} made on {self.created_at}"
