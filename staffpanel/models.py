from django.db import models
from bookings.models import Customer

class DeletedBookingLog(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    table_size = models.IntegerField()
    kids = models.BooleanField()
    time = models.CharField(max_length=10) #stored as a string since timezone is irrelevant
    date = models.DateField()
    special_requests = models.TextField(blank=True, null=True)

    deleted_at = models.DateTimeField(auto_now_add=True)
    deleted_by = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return f"Your booking for: {self.customer} set for the date {self.date} and time {self.time} has been deleted"
    
##later should probably change this to allow different types of logs not just deleted