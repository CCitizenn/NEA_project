from django.contrib import admin
from .models import Booking, Customer

admin.site.register(Booking)
admin.site.register(Customer)

"""
    bookings contains models (which is setting up the forms for /book)
    this is why the 2 models in bookings app must have the admins registered
    this is the same for any app that is created and also contains data that will be managed by staff
"""