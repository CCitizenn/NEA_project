######## This code is without the ability to edit bookings

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Staff Panel</title>
    <style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .controls {
            margin: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            border: 1px solid #ccc;
            padding: 10px;
            text-align: center;
        }

        thead {
            background-color: #ddd;
        }

        tbody {
            display: block;
            overflow: auto;
            width: 100%;
        }

        tr {
            display: table;
            width: 100%;
            table-layout: fixed;
        }

        td {
            max-width: 200px;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }

        /* Sidebar menu */
        .details-sidebar {
            position: fixed;
            top: 0;
            right: -100%;
            width: 35%;
            height: 100%;
            background-color: #f9f9f9;
            box-shadow: -3px 0px 10px rgba(0, 0, 0, 0.2);
            padding: 20px;
            overflow-y: auto;
            transition: right 0.3s ease-in-out;
        }

        .details-sidebar.show {
            right: 0;
        }

        .close-btn {
            position: absolute;
            top: 10px;
            right: 20px;
            font-size: 24px;
            cursor: pointer;
        }

        .details-content {
            margin-top: 40px;
        }

    </style>
</head>
<body>

<div class="controls">
    <button type="button" onclick="changeDate(-1)">←</button>
    <input type="date" id="datePicker" value="{{ selected_date|default:'' }}" onchange="updateDate()">
    <button type="button" onclick="changeDate(1)">→</button>
    <button type="button" onclick="window.location.href='?date={{ today_date }}'">Today</button>
    <button type="button" onclick="window.location.href='?upcoming=true'">Upcoming Bookings</button>

    <label for="sort">Sort by:</label>
    <select name="sort" id="sort" onchange="sortBookings()">
        <option value="" {% if not sort_by %}selected{% endif %}>Default</option>
        <option value="time" {% if sort_by == 'time' %}selected{% endif %}>Time</option>
        <option value="date" {% if sort_by == 'date' %}selected{% endif %}>Date</option>
        <option value="name" {% if sort_by == 'name' %}selected{% endif %}>Name</option>
    </select>
</div>

<table border="1">
    <thead>
        <tr>
            <th>Booking ID</th>
            <th>Customer Name</th>
            <th>Date</th>
            <th>Time</th>
        </tr>
    </thead>
    <tbody>
        {% for booking in bookings %}
        <tr onclick="showDetails(
            '{{ booking.id }}', 
            '{{ booking.customer.name }}', 
            '{{ booking.customer.email }}', 
            '{{ booking.customer.phone }}', 
            '{{ booking.date }}', 
            '{{ booking.time }}', 
            '{{ booking.table_number }}', 
            '{{ booking.special_requests|default:"-" }}'
        )" style="cursor: pointer;">
            <td>{{ booking.id }}</td>
            <td>{{ booking.customer.name }}</td>
            <td>{{ booking.date }}</td>
            <td>{{ booking.time }}</td>
        </tr>
        {% empty %}
        <tr>
            <td colspan="4">No bookings for {{ selected_date }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<!-- Sidebar for booking details -->
<div id="detailsSidebar" class="details-sidebar">
    <span class="close-btn" onclick="closeDetails()">×</span>
    <div class="details-content">
        <h2>Booking Details</h2>
        <p><strong>ID:</strong> <span id="detailId"></span></p>
        <p><strong>Name:</strong> <span id="detailName"></span></p>
        <p><strong>Email:</strong> <span id="detailEmail"></span></p>
        <p><strong>Phone:</strong> <span id="detailPhone"></span></p>
        <p><strong>Date:</strong> <span id="detailDate"></span></p>
        <p><strong>Time:</strong> <span id="detailTime"></span></p>
        <p><strong>Table Number:</strong> <span id="detailTable"></span></p>
        <p><strong>Special Requests:</strong> <span id="detailRequests"></span></p>
    </div>
</div>

<script>

    function showDetails(id, name, email, phone, date, time, table, requests) {
        let sidebar = document.getElementById("detailsSidebar");
    
        document.getElementById("detailId").innerText = id;
        document.getElementById("detailName").innerText = name;
        document.getElementById("detailEmail").innerText = email;
        document.getElementById("detailPhone").innerText = phone;
        document.getElementById("detailDate").innerText = date;
        document.getElementById("detailTime").innerText = time;
        document.getElementById("detailTable").innerText = table;
        document.getElementById("detailRequests").innerText = requests;
    
        sidebar.classList.add("show"); 
    }

    function closeDetails() {
        document.getElementById("detailsSidebar").classList.remove("show");
    }

    document.addEventListener("DOMContentLoaded", function () {
        let datePicker = document.getElementById("datePicker");
    
        if (!datePicker.value) {
            datePicker.value = new Date().toISOString().split("T")[0];
        }
    
        datePicker.addEventListener("change", function () {
            updateDate();
        });
    });
    
    function changeDate(days) {
        let datePicker = document.getElementById("datePicker");
    
        let currentDate = new Date(datePicker.value || new Date().toISOString().split("T")[0]);
        currentDate.setDate(currentDate.getDate() + days);
        
        let newDate = currentDate.toISOString().split("T")[0];
    
        datePicker.value = newDate;
        updateDate();
    }
    
    function updateDate() {
        let datePicker = document.getElementById("datePicker");
        let selectedDate = datePicker.value;
    
        if (selectedDate) {
            updateURL({ date: selectedDate });
        }
    }
    
    function updateURL(newParams) {
        let urlParams = new URLSearchParams(window.location.search);
    
        Object.keys(newParams).forEach(key => {
            if (newParams[key]) {
                urlParams.set(key, newParams[key]);
            } else {
                urlParams.delete(key);
            }
        });
    
        if (urlParams.has("upcoming")) {
            urlParams.set("upcoming", "true");
        }
    
        window.location.href = "?" + urlParams.toString();
    }

    function sortBookings() {
        let sortOption = document.getElementById("sort").value;
        updateURL({ sort: sortOption });
    }

</script>
</body>
</html>

from django.shortcuts import render
from bookings.models import Booking
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime, date
from django.utils.timezone import make_aware
from django.db.models.functions import Lower

@login_required(login_url='/login/')
def staff_panel_view(request):
    if not request.user.is_superuser:
        return HttpResponse("Access Denied: You do not have permission to view this page.", status=403)

    today_date = date.today().strftime("%Y-%m-%d")
    show_upcoming = request.GET.get('upcoming', 'false') == 'true'
    sort_by = request.GET.get('sort', '')

    if show_upcoming:
        bookings = Booking.objects.filter(date__gte=date.today())
        selected_date = None
    else:
        selected_date = request.GET.get('date', today_date)
        try:
            selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponse("Invalid date format.", status=400)
        
        selected_date_aware = make_aware(datetime.combine(selected_date_obj, datetime.min.time()))
        bookings = Booking.objects.filter(date=selected_date_aware)

    # Sort by selected field
    if sort_by == "time":
        bookings = bookings.order_by('time')
    elif sort_by == "date":
        bookings = bookings.order_by('date')
    elif sort_by == "name":
        bookings = bookings.order_by(Lower('customer__name'))  # Lower('Customer__name') because django doesnt handle case of first name so 'Taylor' would come before 'liam' 
    #'Customer__name' with 2 underscores can access related fields in foriegn key relationships.
                                                            
    return render(request, 'staffpanel/staff_panel.html', {
        'bookings': bookings,
        'selected_date': selected_date,
        'show_upcoming': show_upcoming,
        'today_date': today_date,
        'sort_by': sort_by
    })  


**################### This code is half broken trying to make the bookings editable**
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Staff Panel</title>
  <style>
    html, body {
      height: 100%;
      margin: 0;
      padding: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .controls {
      margin: 10px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
    }
    th, td {
      border: 1px solid #ccc;
      padding: 10px;
      text-align: center;
    }
    thead {
      background-color: #ddd;
    }
    tbody {
      display: block;
      overflow: auto;
      width: 100%;
    }
    tr {
      display: table;
      width: 100%;
      table-layout: fixed;
    }
    td {
      max-width: 200px;
      word-wrap: break-word;
      overflow-wrap: break-word;
    }
    /* Sidebar menu */
    .details-sidebar {
      position: fixed;
      top: 0;
      right: -100%;
      width: 35%;
      height: 100%;
      background-color: #f9f9f9;
      box-shadow: -3px 0px 10px rgba(0, 0, 0, 0.2);
      padding: 20px;
      overflow-y: auto;
      transition: right 0.3s ease-in-out;
    }
    .details-sidebar.show {
      right: 0;
    }
    .close-btn {
      position: absolute;
      top: 10px;
      right: 20px;
      font-size: 24px;
      cursor: pointer;
    }
    .details-content {
      margin-top: 40px;
    }
    .edit-controls {
      margin-top: 20px;
    }
    .error {
      color: red;
      font-size: 0.9em;
    }
  </style>
</head>
<body>

<div class="controls">
  <button type="button" onclick="changeDate(-1)">←</button>
  <input type="date" id="datePicker" value="{{ selected_date|default:'' }}" onchange="updateDate()">
  <button type="button" onclick="changeDate(1)">→</button>
  <button type="button" onclick="updateURL({ date: '{{ today_date }}' })">Today</button>
  <button type="button" onclick="updateURL({ upcoming: 'true' })">Upcoming Bookings</button>

  <label for="sort">Sort by:</label>
  <select name="sort" id="sort" onchange="sortBookings()">
    <option value="" {% if not sort_by %}selected{% endif %}>Default</option>
    <option value="time" {% if sort_by == 'time' %}selected{% endif %}>Time</option>
    <option value="date" {% if sort_by == 'date' %}selected{% endif %}>Date</option>
    <option value="name" {% if sort_by == 'name' %}selected{% endif %}>Name</option>
  </select>
</div>

<table border="1">
  <thead>
    <tr>
      <th>Booking ID</th>
      <th>Customer Name</th>
      <th>Date</th>
      <th>Time</th>
    </tr>
  </thead>
  <tbody>
    {% for booking in bookings %}
    <tr onclick="showDetails(
          '{{ booking.id }}',
          '{{ booking.customer.name }}',
          '{{ booking.customer.email }}',
          '{{ booking.customer.phone }}',
          '{{ booking.date }}',
          '{{ booking.time }}',
          '{{ booking.table_number }}',
          '{{ booking.special_requests|default:"-" }}'
        )" style="cursor: pointer;">
      <td>{{ booking.id }}</td>
      <td>{{ booking.customer.name }}</td>
      <td>{{ booking.date }}</td>
      <td>{{ booking.time }}</td>
    </tr>
    {% empty %}
    <tr>
      <td colspan="4">No bookings for {{ selected_date }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>

<!-- Sidebar for booking details and editing -->
<div id="detailsSidebar" class="details-sidebar">
  <span class="close-btn" onclick="closeDetails()">×</span>
  <div class="details-content" id="detailsContent">
    <!-- View mode -->
    <h2>Booking Details</h2>
    <p><strong>ID:</strong> <span id="detailId"></span></p>
    <p><strong>Name:</strong> <span id="detailName"></span></p>
    <p><strong>Email:</strong> <span id="detailEmail"></span></p>
    <p><strong>Phone:</strong> <span id="detailPhone"></span></p>
    <p><strong>Date:</strong> <span id="detailDate"></span></p>
    <p><strong>Time:</strong> <span id="detailTime"></span></p>
    <p><strong>Table Number:</strong> <span id="detailTable"></span></p>
    <p><strong>Special Requests:</strong> <span id="detailRequests"></span></p>
    <div class="edit-controls">
      <button type="button" onclick="enterEditMode()">Edit Booking</button>
    </div>
    <div id="errorMessages" class="error"></div>
  </div>
</div>

<script>
  // ---------- URL Update Functions ----------
  function updateURL(newParams) {
    let urlParams = new URLSearchParams(window.location.search);
    Object.keys(newParams).forEach(key => {
      if (newParams[key]) {
        urlParams.set(key, newParams[key]);
      } else {
        urlParams.delete(key);
      }
    });
    if (urlParams.has("upcoming")) {
      urlParams.set("upcoming", "true");
    }
    window.location.href = "?" + urlParams.toString();
  }
  
  function sortBookings() {
    let sortOption = document.getElementById("sort").value;
    updateURL({ sort: sortOption });
  }

  // ---------- Date Navigation Functions ----------
  document.addEventListener("DOMContentLoaded", function () {
    let datePicker = document.getElementById("datePicker");
    if (!datePicker.value) {
      datePicker.value = new Date().toISOString().split("T")[0];
    }
    datePicker.addEventListener("change", updateDate);
  });
  
  function changeDate(days) {
    let datePicker = document.getElementById("datePicker");
    let currentDate = new Date(datePicker.value || new Date().toISOString().split("T")[0]);
    currentDate.setDate(currentDate.getDate() + days);
    let newDate = currentDate.toISOString().split("T")[0];
    datePicker.value = newDate;
    updateDate();
  }
  
  function updateDate() {
    let datePicker = document.getElementById("datePicker");
    let selectedDate = datePicker.value;
    if (selectedDate) {
      updateURL({ date: selectedDate });
    }
  }

  // ---------- Sidebar and Edit Functions ----------
  function showDetails(id, name, email, phone, date, time, table, requests) {
    // Populate view-mode fields
    document.getElementById("detailId").innerText = id;
    document.getElementById("detailName").innerText = name;
    document.getElementById("detailEmail").innerText = email;
    document.getElementById("detailPhone").innerText = phone;
    document.getElementById("detailDate").innerText = date;
    document.getElementById("detailTime").innerText = time;
    document.getElementById("detailTable").innerText = table;
    document.getElementById("detailRequests").innerText = requests;
    // Ensure view mode is active
    exitEditMode();
    document.getElementById("detailsSidebar").classList.add("show");
  }
  
  function closeDetails() {
    document.getElementById("detailsSidebar").classList.remove("show");
  }
  
  // ---------- Edit Mode Functions ----------
  let currentBookingId = null;
  
  function enterEditMode() {
    currentBookingId = document.getElementById("detailId").innerText;
    let contentDiv = document.getElementById("detailsContent");
    contentDiv.innerHTML = `
      <h2>Edit Booking</h2>
      <form id="editForm">
        <p><strong>ID:</strong> <span id="detailId">${document.getElementById("detailId").innerText}</span></p>
        <p><strong>Name:</strong> <input type="text" id="editName" value="${document.getElementById("detailName").innerText}" required></p>
        <p><strong>Email:</strong> <input type="email" id="editEmail" value="${document.getElementById("detailEmail").innerText}" required></p>
        <p><strong>Phone:</strong> <input type="tel" id="editPhone" value="${document.getElementById("detailPhone").innerText}" required></p>
        <p><strong>Date:</strong> <input type="date" id="editDate" value="${document.getElementById("detailDate").innerText}" required></p>
        <p><strong>Time:</strong> <input type="time" id="editTime" value="${document.getElementById("detailTime").innerText}" required></p>
        <p><strong>Table Number:</strong> <input type="number" id="editTable" value="${document.getElementById("detailTable").innerText}"></p>
        <p><strong>Special Requests:</strong> <textarea id="editRequests" rows="3">${document.getElementById("detailRequests").innerText}</textarea></p>
        <div class="edit-controls">
          <button type="button" onclick="saveBooking()">Save</button>
          <button type="button" onclick="exitEditMode()">Cancel</button>
        </div>
        <div id="errorMessages" class="error"></div>
      </form>
    `;
  }
  
  function exitEditMode(updatedData) {
    // If updatedData is provided, use it; otherwise, fall back on the current view values.
    let id, name, email, phone, date, time, table, requests;
    if (updatedData) {
      id = updatedData.id;
      name = updatedData.name;
      email = updatedData.email;
      phone = updatedData.phone;
      date = updatedData.date;
      time = updatedData.time;
      table = updatedData.table;
      requests = updatedData.requests;
    } else {
      id = document.getElementById("detailId").innerText;
      name = document.getElementById("detailName").innerText;
      email = document.getElementById("detailEmail").innerText;
      phone = document.getElementById("detailPhone").innerText;
      date = document.getElementById("detailDate").innerText;
      time = document.getElementById("detailTime").innerText;
      table = document.getElementById("detailTable").innerText;
      requests = document.getElementById("detailRequests").innerText;
    }
    let contentDiv = document.getElementById("detailsContent");
    contentDiv.innerHTML = `
      <h2>Booking Details</h2>
      <p><strong>ID:</strong> <span id="detailId">${id}</span></p>
      <p><strong>Name:</strong> <span id="detailName">${name}</span></p>
      <p><strong>Email:</strong> <span id="detailEmail">${email}</span></p>
      <p><strong>Phone:</strong> <span id="detailPhone">${phone}</span></p>
      <p><strong>Date:</strong> <span id="detailDate">${date}</span></p>
      <p><strong>Time:</strong> <span id="detailTime">${time}</span></p>
      <p><strong>Table Number:</strong> <span id="detailTable">${table}</span></p>
      <p><strong>Special Requests:</strong> <span id="detailRequests">${requests}</span></p>
      <div class="edit-controls">
          <button type="button" onclick="enterEditMode()">Edit Booking</button>
      </div>
      <div id="errorMessages" class="error"></div>
    `;
  }
  
  function saveBooking() {
    let updatedName = document.getElementById("editName").value.trim();
    let updatedEmail = document.getElementById("editEmail").value.trim();
    let updatedPhone = document.getElementById("editPhone").value.trim();
    let updatedDate = document.getElementById("editDate").value;
    let updatedTime = document.getElementById("editTime").value;
    let updatedTable = document.getElementById("editTable").value;
    let updatedRequests = document.getElementById("editRequests").value.trim();
    let errorDiv = document.getElementById("errorMessages");
    errorDiv.innerText = "";

    // Validate required fields (table number is optional)
    if (!updatedName || !updatedEmail || !updatedPhone || !updatedDate || !updatedTime) {
        errorDiv.innerText = "All fields except table number are required.";
        return;
    }
    if (updatedTable && isNaN(updatedTable)) {
        errorDiv.innerText = "Table Number must be numeric if provided.";
        return;
    }

    let payload = {
        id: currentBookingId,
        name: updatedName,
        email: updatedEmail,
        phone: updatedPhone,
        date: updatedDate,
        time: updatedTime,
        table_number: updatedTable || null,
        special_requests: updatedRequests
    };

    fetch("/staffpanel/edit_booking/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the details in the popout menu
            exitEditMode({
                id: currentBookingId,
                name: updatedName,
                email: updatedEmail,
                phone: updatedPhone,
                date: updatedDate,
                time: updatedTime,
                table: updatedTable || "",
                requests: updatedRequests
            });

            // Update the booking row in the table
            let row = document.querySelector(`[data-booking-id='${currentBookingId}']`);
            if (row) {
                row.querySelector(".booking-name").innerText = updatedName;
                row.querySelector(".booking-email").innerText = updatedEmail;
                row.querySelector(".booking-phone").innerText = updatedPhone;
                row.querySelector(".booking-date").innerText = updatedDate;
                row.querySelector(".booking-time").innerText = updatedTime;
                row.querySelector(".booking-table").innerText = updatedTable || "N/A";
                row.querySelector(".booking-requests").innerText = updatedRequests;
            }
        } else {
            errorDiv.innerText = data.error || "An error occurred.";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        errorDiv.innerText = "An error occurred while updating the booking.";
    });
}
  // Helper to retrieve CSRF token
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      let cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
</script>

</body>
</html>

URLS.py
[
    path('edit_booking/', edit_booking, name='edit_booking'),
]
VIEWS.py
from django.shortcuts import render
from bookings.models import Booking,Customer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime, date
from django.utils.timezone import make_aware
from django.db.models.functions import Lower

import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # or ensure CSRF token is passed


@login_required(login_url='/login/')
def staff_panel_view(request):
    if not request.user.is_superuser:
        return HttpResponse("Access Denied: You do not have permission to view this page.", status=403)

    today_date = date.today().strftime("%Y-%m-%d")
    show_upcoming = request.GET.get('upcoming', 'false') == 'true'
    sort_by = request.GET.get('sort', '')

    if show_upcoming:
        bookings = Booking.objects.filter(date__gte=date.today())
        selected_date = None
    else:
        selected_date = request.GET.get('date', today_date)
        try:
            selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponse("Invalid date format.", status=400)
        
        selected_date_aware = make_aware(datetime.combine(selected_date_obj, datetime.min.time()))
        bookings = Booking.objects.filter(date=selected_date_aware)

    # Sort by selected field
    if sort_by == "time":
        bookings = bookings.order_by('time')
    elif sort_by == "date":
        bookings = bookings.order_by('date')
    elif sort_by == "name":
        bookings = bookings.order_by(Lower('customer__name'))  # Lower('Customer__name') because django doesnt handle case of first name so 'Taylor' would come before 'liam' 
    #'Customer__name' with 2 underscores can access related fields in foriegn key relationships.
                                                            
    return render(request, 'staffpanel/staff_panel.html', {
        'bookings': bookings,
        'selected_date': selected_date,
        'show_upcoming': show_upcoming,
        'today_date': today_date,
        'sort_by': sort_by
    })  


@require_POST
def edit_booking(request):
    try:
        data = json.loads(request.body)
        booking_id = data.get("id")
        # Fetch the booking record
        booking = Booking.objects.get(id=booking_id)
        
        # Update the related customer fields
        customer = booking.customer
        customer.name = data.get("name")
        customer.email = data.get("email")
        customer.phone = data.get("phone")
        customer.save()
        
        # Update booking fields. Allow table_number to be null if not provided.
        booking.date = data.get("date")
        booking.time = data.get("time")
        booking.table_number = data.get("table_number") if data.get("table_number") != "" else None
        booking.special_requests = data.get("special_requests")
        booking.save()
        
        return JsonResponse({"success": True})
    except Booking.DoesNotExist:
        return JsonResponse({"success": False, "error": "Booking not found."})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})