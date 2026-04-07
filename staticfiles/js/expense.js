let expenseList = [];

// LOAD DATA
function loadExpenses(date = "") {

    let url = "/expense/";
    if (date) url += `?date=${date}`;

    fetch(url, {
        headers: { "X-Requested-With": "XMLHttpRequest" }
    })
    .then(res => res.json())
    .then(data => {
        expenseList = data.data;
        renderTable();
    });
}

// RENDER TABLE
function renderTable() {

    let tbody = document.getElementById("expenseBody");
    tbody.innerHTML = "";

    let total = 0;

    expenseList.forEach((e, i) => {

        total += parseFloat(e.amount);

        tbody.innerHTML += `
        <tr>
            <td>${i + 1}</td>
            <td>${e.date}</td>
            <td contenteditable="true" onblur="editExpense(${e.id}, this, 'title')">${e.title}</td>
            <td contenteditable="true" onblur="editExpense(${e.id}, this, 'amount')">₹ ${e.amount}</td>
            <td>
                <button onclick="deleteExpense(${e.id})" class="btn-delete">🗑</button>
            </td>
        </tr>
        `;
    });

    document.getElementById("totalExpense").innerText = total.toFixed(2);
}

// ADD
function addExpense() {

    let date = document.getElementById("expDate").value;
    let title = document.getElementById("expTitle").value;
    let amount = document.getElementById("expAmount").value;

    if (!date || !title || !amount) {
        alert("Fill all fields!");
        return;
    }

    fetch("/expense/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ date, title, amount })
    })
    .then(() => {
        loadExpenses();
        clearForm();
    });
}

// EDIT
function editExpense(id, el, field) {

    let value = el.innerText.replace("₹", "").trim();

    let exp = expenseList.find(e => e.id === id);

    if (field === "title") exp.title = value;
    if (field === "amount") exp.amount = value;

    fetch("/expense/", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify(exp)
    });
}

// DELETE
function deleteExpense(id) {

    fetch("/expense/", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ id })
    })
    .then(() => loadExpenses());
}

// FILTER
function filterExpense() {
    let date = document.getElementById("filterDate").value;
    loadExpenses(date);
}

// CLEAR FORM
function clearForm() {
    document.getElementById("expTitle").value = "";
    document.getElementById("expAmount").value = "";
}

// CSRF
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// INIT
window.onload = () => {
    document.getElementById("expDate").valueAsDate = new Date();
    loadExpenses();
};