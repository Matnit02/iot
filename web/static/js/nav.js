function openMenu() {
    document.getElementById("sidebar").style.width = "250px";
    document.body.classList.add("sidebar-open"); // Adjusts main content
}

function closeMenu() {
    document.getElementById("sidebar").style.width = "0";
    document.body.classList.remove("sidebar-open");
}
