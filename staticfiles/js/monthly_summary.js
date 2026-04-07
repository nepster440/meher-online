// ===== MONTHLY SUMMARY JS (FINAL) =====

window.addEventListener("DOMContentLoaded", () => {

    // ===== ELEMENTS =====
    const monthSelect = document.getElementById("monthSelect");
    const yearSelect = document.getElementById("yearSelect");

    if (!monthSelect || !yearSelect) return;

    // ===== GET SELECTED VALUES FROM DJANGO =====
    let selectedMonth = document.getElementById("selectedMonth")?.value;
    let selectedYear = document.getElementById("selectedYear")?.value;

    // ===== DEFAULT (AGAR NA MILE TO CURRENT) =====
    const today = new Date();

    if (!selectedMonth) selectedMonth = today.getMonth() + 1;
    if (!selectedYear) selectedYear = today.getFullYear();

    // Convert to number
    selectedMonth = parseInt(selectedMonth);
    selectedYear = parseInt(selectedYear);

    // ===== RESET OPTIONS (IMPORTANT FIX) =====
    monthSelect.innerHTML = "";
    yearSelect.innerHTML = "";

    // ===== MONTH LIST =====
    const months = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ];

    months.forEach((month, index) => {

        const option = document.createElement("option");

        option.value = index + 1;
        option.textContent = month;

        if ((index + 1) === selectedMonth) {
            option.selected = true;
        }

        monthSelect.appendChild(option);
    });

    // ===== YEAR LIST =====
    const currentYear = today.getFullYear();

    for (let y = currentYear; y >= currentYear - 5; y--) {

        const option = document.createElement("option");

        option.value = y;
        option.textContent = y;

        if (y === selectedYear) {
            option.selected = true;
        }

        yearSelect.appendChild(option);
    }

    // ===== FILTER FUNCTION (GLOBAL) =====
    window.filterData = function () {

        const selectedM = monthSelect.value;
        const selectedY = yearSelect.value;

        // Debug (optional)
        console.log("Filter:", selectedM, selectedY);

        // Redirect with query params
        window.location.href = `?month=${selectedM}&year=${selectedY}`;
    };

});


function exportExcel() {
    const m = document.getElementById("monthSelect").value;
    const y = document.getElementById("yearSelect").value;

    window.location.href = `/monthly/export/?month=${m}&year=${y}`;
}