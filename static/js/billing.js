/**
 * 🚀 BILLING SYSTEM - FINAL ROBUST SCRIPT
 * Fixes: Click issues, Calculation bugs, and Row management
 */

(function() {
    // 1. CALCULATE FUNCTION (Window scope taaki HTML se access ho sake)
    window.calculateTotal = function() {
        let grandTotal = 0;
        const rows = document.querySelectorAll("#billBody tr");

        rows.forEach(row => {
            const qtyInput = row.querySelector(".qty");
            const priceInput = row.querySelector(".price");
            const totalDisplay = row.querySelector(".row-total");

            if (qtyInput && priceInput && totalDisplay) {
                const qty = parseFloat(qtyInput.value) || 0;
                const price = parseFloat(priceInput.value) || 0;
                const total = qty * price;

                totalDisplay.innerText = total.toFixed(2);
                grandTotal += total;
            }
        });

        const grandTotalElement = document.getElementById("grandTotal");
        if (grandTotalElement) {
            grandTotalElement.innerText = grandTotal.toFixed(2);
        }
    };

    // 2. ADD ROW FUNCTION
    window.addRow = function() {
        console.log("Add Row Triggered");
        const tbody = document.getElementById("billBody");
        const rowCount = tbody.rows.length + 1;

        const rowHTML = `
        <tr>
            <td class="row-no">${rowCount}</td>
            <td><input type="text" class="input service-name" placeholder="Enter service..."></td>
            <td><input type="number" class="input qty" value="1"></td>
            <td><input type="number" class="input price" value="0"></td>
            <td class="row-total">0.00</td>
            <td>
                <button type="button" onclick="window.deleteRow(this)" class="btn-delete">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </td>
        </tr>`;

        tbody.insertAdjacentHTML("beforeend", rowHTML);
        window.calculateTotal();
    };

    // 3. DELETE ROW FUNCTION
    window.deleteRow = function(btn) {
        const tbody = document.getElementById("billBody");
        if (tbody.rows.length > 1) {
            btn.closest("tr").remove();
            // Update serial numbers
            document.querySelectorAll(".row-no").forEach((td, i) => td.innerText = i + 1);
            window.calculateTotal();
        } else {
            alert("Kam se kam ek row rehni chahiye!");
        }
    };

    // 4. SAVE BILL FUNCTION
    window.saveBill = async function() {
        const customer = document.getElementById("customer").value;
        const total = document.getElementById("grandTotal").innerText;
        const items = [];

        document.querySelectorAll("#billBody tr").forEach(row => {
            const name = row.querySelector(".service-name").value;
            const qty = row.querySelector(".qty").value;
            const price = row.querySelector(".price").value;

            if (name.trim() !== "") {
                items.push({ name, qty, price });
            }
        });

        if (!customer) return alert("Pehle Customer ka naam likho!");
        if (items.length === 0) return alert("Kam se kam ek valid service item daalo!");

        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value;
        if (!csrfToken) return alert("CSRF Token missing! Page refresh karein.");

        try {
            const response = await fetch("/billing/", {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json", 
                    "X-CSRFToken": csrfToken 
                },
                body: JSON.stringify({ customer, items, total })
            });

            const data = await response.json();
            if (data.status === "success") {
                document.getElementById("displayInvoice").innerText = "Invoice: " + data.invoice_no;
                alert("✅ Bill Saved! Invoice No: " + data.invoice_no);
            } else {
                alert("❌ Save failed: " + (data.message || "Unknown error"));
            }
        } catch (e) {
            console.error(e);
            alert("Save karne mein error aaya! Console check karein.");
        }
    };

    // 5. PRINT PDF FUNCTION
    window.downloadPDF = async function() {
        const customer = document.getElementById("customer").value;
        const total = document.getElementById("grandTotal").innerText;
        
        if (!customer) return alert("Pehle Customer Name likho!");

        const items = [];
        document.querySelectorAll("#billBody tr").forEach(row => {
            const name = row.querySelector(".service-name").value;
            if (name.trim() !== "") {
                items.push({
                    name: name,
                    qty: row.querySelector(".qty").value,
                    price: row.querySelector(".price").value
                });
            }
        });

        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value;

        try {
            const response = await fetch("/billing/invoice/", {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json", 
                    "X-CSRFToken": csrfToken 
                },
                body: JSON.stringify({ customer, items, total })
            });

            if (!response.ok) throw new Error("PDF generate nahi ho saka");

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `Invoice_${customer.replace(/\s+/g, '_')}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (e) {
            alert("PDF Download Error: " + e.message);
        }
    };

    // 6. EVENT LISTENERS
    // Input listener for live calculation
    document.addEventListener("input", function(e) {
        if (e.target.classList.contains("qty") || e.target.classList.contains("price")) {
            window.calculateTotal();
        }
    });

    // Page Load par pehla calculation
    document.addEventListener("DOMContentLoaded", () => {
        window.calculateTotal();
    });

})();

// INITIAL CALULATION FIX
setTimeout(() => {
    window.calculateTotal();
}, 300); // 300ms delay to ensure DOM is fully loaded