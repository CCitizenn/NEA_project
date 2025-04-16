/*function handles the popout menu from the left of the screen to show more about customer details*/
let lastShownBookingId = null;
function showDetails(id, name, email, phone, date, time, table, requests, completed) {
    const sidebar = document.getElementById("detailsSidebar");

    // some toggle logic so that when you click a customer detail again, it closes it 
    if (sidebar.classList.contains("show") && lastShownBookingId === id) {
        closeDetails();
        lastShownBookingId = null;
        return;
    }

    // Set new booking details
    document.getElementById("detailId").innerText = id;
    document.getElementById("detailName").innerText = name;
    document.getElementById("detailEmail").innerText = email;
    document.getElementById("detailPhone").innerText = phone;
    document.getElementById("detailDate").innerText = date;
    document.getElementById("detailTime").innerText = time;
    document.getElementById("detailTableSize").innerText = table;
    document.getElementById("detailRequests").innerText = requests;

    // Update form action
    const form = document.getElementById("completeForm");
    form.action = `/staffpanel/mark_completed/${id}/`;

    const deleteForm = document.getElementById("deleteForm");
    deleteForm.action = `/staffpanel/delete/${id}/`;

    // Update button text
    const button = document.getElementById("completeBtn");
    button.innerText = (completed === 'true') ? "Mark as Incomplete" : "Mark as Completed";

    // Show sidebar
    sidebar.classList.add("show");
    lastShownBookingId = id;

    // Edit details button
    const editForm = document.getElementById("editForm");
    editForm.action = `/staffpanel/edit/${id}/`;
}


/*just allows you to use esc to exit that menu*/
document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
        closeDetails();
        lastShownBookingId = null;
    }
});

/*closes the sidebar*/
function closeDetails() {
    document.getElementById("detailsSidebar").classList.remove("show");
}

/*initializes the datepicker to today for staff panel- then allows you to chose your own via calandar*/ 
document.addEventListener("DOMContentLoaded", function () {
    //"DOMContentLoaded" waits for the HTML DOM to load onto browser before executing the JS
    let datePicker = document.getElementById("datePicker");

    if (!datePicker.value) {
        datePicker.value = new Date().toISOString().split("T")[0];
    }

    datePicker.addEventListener("change", function () {
        updateDate();
    });
});

/* this function handles the <- and -> keys that are add and subtract the day to allow staff to "scroll" through days*/
function changeDate(days) {
    let datePicker = document.getElementById("datePicker");

    let currentDate = new Date(datePicker.value || new Date().toISOString().split("T")[0]);
    currentDate.setDate(currentDate.getDate() + days);
    
    let newDate = currentDate.toISOString().split("T")[0];

    datePicker.value = newDate;
    updateDate();
}

/* calls updateURL() and grabs the selected day so that it can show the selected day*/
function updateDate() {
    let datePicker = document.getElementById("datePicker");
    let selectedDate = datePicker.value;

    if (selectedDate) {
        updateURL({ date: selectedDate });
    }
}

function updateURL(newParams) {
    let urlParams = new URLSearchParams(window.location.search); //gets the current URL that is in the browser via URLSearchParams API

    Object.keys(newParams).forEach(key => {
        if (newParams[key]) {
            urlParams.set(key, newParams[key]);
        } else {
            urlParams.delete(key);
        }
    });

    if (!("upcoming" in newParams)) {
        urlParams.delete("upcoming");
    }

    window.location.href = "?" + urlParams.toString();
}

// so staff can organize by certain choices like date, time etc...
function sortBookings() {
    let sortOption = document.getElementById("sort").value;
    updateURL({ sort: sortOption });
}
