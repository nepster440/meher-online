function toggleTheme() {
    let body = document.body;
    let icon = document.getElementById("themeIcon");

    body.classList.toggle("dark-mode");

    let isDark = body.classList.contains("dark-mode");
    localStorage.setItem("theme", isDark);

    // Icon change
    if (isDark) {
        icon.classList.remove("fa-moon");
        icon.classList.add("fa-sun");
    } else {
        icon.classList.remove("fa-sun");
        icon.classList.add("fa-moon");
    }

    // Re-render chart if exists
    if (typeof renderChart === "function") {
        renderChart(labels, data);
    }
}

/* ===== LOAD THEME SAFELY ===== */
document.addEventListener("DOMContentLoaded", function () {
    let body = document.body;
    let icon = document.getElementById("themeIcon");

    let savedTheme = localStorage.getItem("theme");

    if (savedTheme === "true") {
        body.classList.add("dark-mode");
        icon.classList.remove("fa-moon");
        icon.classList.add("fa-sun");
    } else {
        body.classList.remove("dark-mode");
        icon.classList.remove("fa-sun");
        icon.classList.add("fa-moon");
    }
});