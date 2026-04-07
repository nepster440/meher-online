window.onload = function () {

    const yearSelect = document.getElementById("yearSelect");

    let currentYear = new Date().getFullYear();

    for (let y = currentYear; y >= currentYear - 5; y--) {
        let option = new Option(y, y);
        yearSelect.add(option);
    }

    renderChart();
};

function filterYear() {
    let y = document.getElementById("yearSelect").value;
    window.location.href = `?year=${y}`;
}

