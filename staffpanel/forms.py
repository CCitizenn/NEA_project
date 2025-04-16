import re
from datetime import date
from django import forms
from bookings.models import Booking, Customer
from django.utils import timezone

class EditBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'table_size', 'kids', 'special_requests', 'completed']

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.localdate():
            raise forms.ValidationError("Booking can't be a date in the past. The kitchen would be unhappy...")
        return date

    
    def clean_time(self):
        timeString = self.cleaned_data['time']

        #firstly lets test the given time against a regular expression wanting it in a hh:mm formate
        if not re.match(r"^\d{2}:\d{2}$", timeString):
            raise forms.ValidationError("please format correctly")

        hourString, minuteString = timeString.split(":") 
        #split the time into 2 different variables for hour and minute
        if not hourString.isdigit() or not minuteString.isdigit():
            raise forms.ValidationError("Time must contain numbers only.")
        
        #cast from strings to integers
        hour = int(hourString)
        minute = int(minuteString)

        # then make sure its within the acceptable open times- unless theyre trying to help prep
        if hour < 16 or hour > 21 or minute < 0 or minute > 59:
            raise forms.ValidationError("Bookings must be between 16:00 and 21:00.")
        if hour == 21 and minute > 0:
            raise forms.ValidationError("Last booking time is 21:00.")
        
        return timeString
    
    def save(self):
        # Save the booking data (excluding customer fields)
        booking = super().save(commit=False)
        booking.save()
        return booking
    
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email'] 