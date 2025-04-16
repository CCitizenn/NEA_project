import re
from datetime import date
from django.core.exceptions import ValidationError
from django import forms
from .models import Booking

def validate_phone_num(value):
    stripped_value = value.replace(' ', '') 
    pattern = r'^(\+447\d{9}|\+441\d{9}|\+442\d{9}|07\d{9}|01\d{9}|02\d{9})$'
    # ^ and $ at start and end respectively say all of it must match- not just some
    # \+447\d{9} says it can be +447 followed by 9 digits
    # | counts as or, then following counts for differnt uk numbers, landlines etc to account for older pepple :P

    if not re.match(pattern, stripped_value):
        raise ValidationError("Enter a valid UK phone number, e.g. 07123 456789 or +44 191 1234567")

def validate_future_date(value):
    if value < date.today():
        raise ValidationError("The date must be in the future.")

class BookingForm(forms.ModelForm):
    #shows the actual value held in the database whereas what is displayed to the user
    TBLSIZE = [
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), 
        ('6', '6'), ('7', '7'), ('8', '8'), ('9+', 'Over 8'),
    ]
    TIME_CHOICES = [
        ('16:00', '4 PM'), ('16:15', '4:15 PM'), ('16:30', '4:30 PM'), ('16:45', '4:45 PM'),
        ('17:00', '5 PM'), ('17:15', '5:15 PM'), ('17:30', '5:30 PM'), ('17:45', '5:45 PM'),
        ('18:00', '6 PM'), ('18:15', '6:15 PM'), ('18:30', '6:30 PM'), ('18:45', '6:45 PM'),
        ('19:00', '7 PM'), ('19:15', '7:15 PM'), ('19:30', '7:30 PM'), ('19:45', '7:45 PM'),
        ('20:00', '8 PM'), ('20:15', '8:15 PM'), ('20:30', '8:30 PM'), ('20:45', '8:45 PM'),
        ('21:00', '9 PM'),
    ]
    
    name = forms.CharField(max_length=255)
    phone = forms.CharField(
        max_length=15,
        validators=[validate_phone_num],
        help_text="Must be a UK phone landline or mobile"
    )
    email = forms.EmailField()
    table_size = forms.ChoiceField(
        choices=TBLSIZE,
        widget=forms.Select(attrs={'id': 'tableSize'})
    )
    kids = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'tickbox'})
    )
    time = forms.ChoiceField(choices=TIME_CHOICES)
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
        input_formats=['%Y-%m-%d'],
        validators=[validate_future_date],
        help_text="Must be a date in the future. Unless you have a time machine....."
    )
    special_requests = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'special requests...'}), 
        required=False  # (optional)
    )
    # nested class configuring the form so you dont have to do it yourself.
    class Meta:
        model = Booking
        fields = ['name', 'phone', 'email', 'table_size', 'kids', 'time', 'date', 'special_requests']

