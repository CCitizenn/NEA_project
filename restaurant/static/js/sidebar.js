function toggleSidebar() {
    const sidebar = document.getElementById("staffSidebar");
    const overlay = document.getElementById("overlay");
    //code to handle it popping out, first deciding whether its already there or not
    if (sidebar.style.left === "0px") {
        sidebar.style.left = "-250px";
        overlay.classList.remove("active");
    } else {
        sidebar.style.left = "0px";
        overlay.classList.add("active");
    }
}