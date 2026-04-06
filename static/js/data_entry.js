/* ===== UTILS ===== */
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

/* ===== CALCULATIONS ===== */
function calculateRow(row) {
    let inputs = row.querySelectorAll(".input");
    let total = 0;

    inputs.forEach(input => {
        total += parseFloat(input.value) || 0;
    });

    row.querySelector(".row-total").innerText = total;
}

function calculateGrandTotal() {
    let totals = document.querySelectorAll(".row-total");
    let grand = 0;

    totals.forEach(t => {
        grand += parseFloat(t.innerText) || 0;
    });

    document.getElementById("grandTotal").innerText = grand;
}

/* ===== EVENTS ===== */
function attachEvents(row) {
    let inputs = row.querySelectorAll(".input");

    inputs.forEach((input, index) => {

        input.addEventListener("input", () => {
            calculateRow(row);
            calculateGrandTotal();
        });

        // 🔥 ENTER → next row
        if (index === 7) {
            input.addEventListener("keydown", (e) => {
                if (e.key === "Enter") {
                    e.preventDefault();

                    let nextRow = row.nextElementSibling;

                    if (!nextRow) {
                        addRow();
                    } else {
                        nextRow.querySelectorAll(".input")[0].focus();
                    }
                }
            });
        }
    });
}

/* ===== ADD ROW ===== */
function addRow(data = null) {
    let table = document.getElementById("tableBody");
    let rowCount = table.rows.length + 1;

    let newRow = document.createElement("tr");

    newRow.innerHTML = `
    <td>${rowCount}</td>
    <td><input type="number" class="form-control input" value="${data ? data.xe : 0}"></td>
    <td><input type="number" class="form-control input" value="${data ? data.press : 0}"></td>
    <td><input type="number" class="form-control input" value="${data ? data.online : 0}"></td>
    <td><input type="number" class="form-control input" value="${data ? data.color : 0}"></td>
    <td><input type="number" class="form-control input" value="${data ? data.xg : 0}"></td>
    <td><input type="number" class="form-control input" value="${data ? data.pg : 0}"></td>
    <td><input type="number" class="form-control input" value="${data ? data.og : 0}"></td>
    <td><input type="number" class="form-control input" value="${data ? data.cg : 0}"></td>
    <td class="row-total">0</td>
    <td>
        <button class="btn-delete" onclick="deleteRow(this)">
            <i class="fa-solid fa-trash"></i>
        </button>
    </td>`;

    table.appendChild(newRow);

    attachEvents(newRow);
    calculateRow(newRow);

    newRow.querySelectorAll(".input")[0].focus();
}

/* ===== DELETE ===== */
function deleteRow(btn) {
    let row = btn.closest("tr");
    row.remove();
    updateRowNumbers();
    calculateGrandTotal();
}

function updateRowNumbers() {
    let rows = document.querySelectorAll("#tableBody tr");

    rows.forEach((row, index) => {
        row.cells[0].innerText = index + 1;
    });
}

/* ===== FETCH DATA ===== */
function fetchDataByDate() {
    let date = document.getElementById("selectedDate").value;

    if (!date) return;

    fetch(`/data/fetch-data/?date=${date}`)  // ✅ FIXED URL
        .then(res => res.json())
        .then(response => {

            let table = document.getElementById("tableBody");
            table.innerHTML = "";

            if (response.data && response.data.length > 0) {

                response.data.forEach(item => addRow(item));

            } else {
                addRow();
            }

            calculateGrandTotal();
        })
        .catch(err => console.error("Fetch Error:", err));
}

/* ===== SAVE DATA ===== */
function saveData() {
    let rows = document.querySelectorAll("#tableBody tr");
    let selectedDate = document.getElementById("selectedDate").value;

    if (!selectedDate) {
        alert("⚠️ Please select date first");
        return;
    }

    let data = [];

    rows.forEach(row => {
        let inputs = row.querySelectorAll(".input");

        data.push({
            date: selectedDate,
            xe: inputs[0].value || 0,
            press: inputs[1].value || 0,
            online: inputs[2].value || 0,
            color: inputs[3].value || 0,
            xg: inputs[4].value || 0,
            pg: inputs[5].value || 0,
            og: inputs[6].value || 0,
            cg: inputs[7].value || 0,
        });
    });

    fetch(window.location.href, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            alert("✅ Data Saved Successfully!");
            fetchDataByDate(); // 🔥 reload data without refresh
        } else {
            alert("❌ Error saving data");
        }
    })
    .catch(err => {
        console.error(err);
        alert("❌ Network Error");
    });
}

/* ===== INIT ===== */
document.addEventListener("DOMContentLoaded", () => {

    let dateInput = document.getElementById("selectedDate");

    // Default = Today
    if (dateInput && !dateInput.value) {
        dateInput.value = new Date().toISOString().split('T')[0];
    }

    // 🔥 AUTO LOAD DATA
    fetchDataByDate();
});