from django.shortcuts import render, get_object_or_404, redirect
from bookings.models import Booking, BookingData
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from datetime import datetime, date, timedelta
from django.utils.timezone import make_aware
from django.db.models.functions import Lower
from django.core.mail import send_mail
from django.contrib import messages
from .models import DeletedBookingLog 
from .forms import EditBookingForm, CustomerForm
from django.conf import settings
from django.db.models import Count

@login_required(login_url='/login/')
def staff_panel_view(request):
    #the server checks if logged in account is registered superuser (Staff/admin)
    if not request.user.is_superuser:
        return HttpResponse("Access Denied: You do not have permission to view this page.", status=403)

    today_date = date.today().strftime("%Y-%m-%d")
    show_upcoming = request.GET.get('upcoming', 'false') == 'true'
    sort_by = request.GET.get('sort', '')

    if show_upcoming:
        bookings = Booking.objects.filter(date__gte=date.today())
        selected_date = None
        # if show_upcoming, then show all available bookings
    else: 
        selected_date = request.GET.get('date', today_date)
        try:
            selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponse("Invalid date format.", status=400)
        
        selected_date_aware = make_aware(datetime.combine(selected_date_obj, datetime.min.time()))
        bookings = Booking.objects.filter(date=selected_date_aware)
        #else, show the bookings only available on one specific date

    if sort_by == "time":
        bookings = bookings.order_by('time')
    elif sort_by == "date":
        bookings = bookings.order_by('date')
    elif sort_by == "name":
        bookings = bookings.order_by(Lower('customer__name'))  
    # Lower('Customer__name') because django doesnt handle cases when sorting so 'Taylor' would come before 'liam' 
    #'customer__name' with 2 underscores can access related fields in foriegn key relationships.
                                                            
    return render(request, 'staffpanel/staff_panel.html', {
        'bookings': bookings,
        'selected_date': selected_date,
        'show_upcoming': show_upcoming,
        'today_date': today_date,
        'sort_by': sort_by
    })  

def mark_completed(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.completed = not booking.completed
    booking.save()
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

def is_staff_user(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_staff_user) #only staff should be able to delete bookings (although already checks it improves security)
def delete_booking(request, booking_id): #deleting test with given booking ID
    booking= get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST': #preventing accidental deletion by restricting to only POST

        customer = booking.customer
        customer_email = customer.email
        customer_name = customer.name
        booking_date = booking.date
        booking_time = booking.time

        #make a copy, and add it to DeletedBookingLog so that there is logs on staffpanel/deleted_log
        DeletedBookingLog.objects.create(
            customer=customer,
            table_size=booking.table_size,
            kids=booking.kids,
            time=booking.time,
            date=booking.date,
            special_requests=booking.special_requests,
        )

        send_mail(
            subject="Your Booking at Pacinos, South Shields, has been cancelled :(",
            message=(
                f"Dear {customer.name},\n\n"
                f"Your booking for {booking.date} at {booking.time} has been cancelled by our staff.\n"
                f"If you believe this to be a mistake, please give us a call during our open hours."
            ),
            from_email=settings.EMAIL_HOST_USER,  
            recipient_list=[customer_email],
            fail_silently=False,
        )
        messages.success(request, "Booking deleted. :P")
        booking.delete()
        return redirect('staffpanel:staff_panel')
    return redirect('staffpanel:staff_panel')

@user_passes_test(is_staff_user)
def deleted_bookings_log(request):
    logs = DeletedBookingLog.objects.all().order_by('-deleted_at')
    return render(request, 'staffpanel/deleted_log.html', {'logs': logs})


def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST': # again, to prevent accidental edits to booking whcih could cause problems down the line
        form = EditBookingForm(request.POST, instance=booking)
        customer_form = CustomerForm(request.POST, instance=booking.customer)
        if form.is_valid() and customer_form.is_valid():
            form.save()
            customer_form.save()
            messages.success(request, 'Booking and customer updated successfully.')
            return redirect('staffpanel:staff_panel')
    else:
        form = EditBookingForm(instance=booking) #this means that i dont have to manually define the prefilled details using def set_initial_data(self, booking) in the forms page
        customer_form = CustomerForm(instance=booking.customer)
    
    return render(request, 'staffpanel/edit_booking.html', {
        'form': form,
        'customer_form': customer_form,
        'booking': booking
    })

###
def analytics_view(request):
    today = datetime.today()
    start_week = today - timedelta(days=today.weekday())  #set to monday
    end_week = start_week + timedelta(days=6)


    weekly_bookings = BookingData.objects.filter(
        created_at__date__range=[start_week.date(), end_week.date()]
    )


    daily_counts = weekly_bookings.values('day_of_week').annotate(total=Count('id'))

    peak_times = weekly_bookings.values('booking_time__hour').annotate(count=Count('id')).order_by('-count')[:5]

    for peak_time in peak_times:
        hour = peak_time['booking_time__hour']
        if hour == 0:
            peak_time['formatted_time'] = '12 AM'
        elif hour < 12:
            peak_time['formatted_time'] = f'{hour} AM'
        elif hour == 12:
            peak_time['formatted_time'] = '12 PM'
        else:
            peak_time['formatted_time'] = f'{hour - 12} PM'

    total_weekly = weekly_bookings.count()
    avg_per_day = round(total_weekly / 7, 2)

    context = {
        'daily_counts': daily_counts,
        'peak_times': peak_times,
        'total_weekly': total_weekly,
        'avg_per_day': avg_per_day,
        'start_week': start_week.date(),
        'end_week': end_week.date()
    }

    return render(request, 'staffpanel/analytics.html', context)

