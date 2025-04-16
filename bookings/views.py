from django.shortcuts import render, redirect
from .models import Booking, Customer
from .forms import BookingForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'bookings/index.html')

@login_required
def booking_view(request):
    if request.method == 'POST': #django validates the data when form is submitted "POST"
        form = BookingForm(request.POST)
        if form.is_valid():
            # Get customer details
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']

            #create customer
            customer = Customer.objects.create(name=name, phone=phone, email=email)

            # Create a new booking
            booking = form.save(commit=False)
            booking.customer = customer  
            booking.save()

            # Email
            email_subject = 'Pacinos Booking Confirmation'
            email_main_message = f'Thank you for your booking, {name}!\n' \
                      f'We look forward to seeing you! We hope to make your evening as enjoyable as possible.\n' \
                      f'Your reservation is confirmed for {booking.date} at {booking.time} for {booking.table_size} people.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(email_subject, email_main_message, from_email, recipient_list)

            return redirect('success')
        else:
            # debugging measure --> sends errors to the terminal so i can show people what im crying about
            print(form.errors) 
    else:
        form = BookingForm()

    return render(request, 'bookings/booking_form.html', {'form': form})

# view just returning success.html template 
def success_view(request):
    return render(request, 'bookings/success.html')

# view is for the "show bookings" so that customers can view any made bookings
# admittedly this part doesnt work too great but i am short on time
def user_bookings(request):
    # 'manually' check if the user is logged in
    if not request.user.is_authenticated:
        return redirect("login:login") 
    try:
        customer = Customer.objects.get(email=request.user.email) 
        bookings = Booking.objects.filter(customer=customer)  # filter bookings by the Customer logged in
    except Customer.DoesNotExist:
        bookings = []  # when no customer exists -> return an empty list ie; no bookings
    return render(request, "bookings/user_bookings.html", {"bookings": bookings})