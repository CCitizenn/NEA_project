/* Prevents form submission for tables over size of 7 */
function validateForm(event) {
var tableSize = document.querySelector("[name='table_size']").value;
if (tableSize === "9+") {
    alert("Unfortunately, we cannot take bookings for over 8 people via the website. Please call us directly on 0191 456 1089 during open hours to discuss the booking with staff.");
    event.preventDefault(); 
}
}
/* prevents multiple form requests- this prevents duplicate bookings in staff panel */
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("bookingForm");
    const submitBtn = document.getElementById("submitBtn");

    form.addEventListener("submit", function () {
        submitBtn.disabled = true;
    });
});

/*loads the custom date picker loaded at top of form (mostly for looks)*/
document.addEventListener('DOMContentLoaded', function() {
    flatpickr('.datepicker', {
        minDate: "today",  
        dateFormat: "Y-m-d",  
    });
});

/*the drop down menu for the table size*/ 
document.addEventListener("DOMContentLoaded", function () {
    var tableSizeDropdown = document.querySelector("[name='table_size']");
    if (tableSizeDropdown) {
        tableSizeDropdown.id = "tableSize";
    }
});