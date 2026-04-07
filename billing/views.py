from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import Bill, BillItem
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
import json, os
from django.conf import settings
from datetime import datetime
from django.shortcuts import render
from .models import Bill, BillItem
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.platypus import *
from num2words import num2words
import json, os, qrcode
from django.contrib.auth.mixins import LoginRequiredMixin


# ✅ CREATE BILL
class BillingView(LoginRequiredMixin, TemplateView):
    template_name = "billing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Find Customer ke liye purane customers bhejna
        context['customers'] = Bill.objects.values_list('customer_name', flat=True).distinct()
        return context
    
    def post(self, request):
        try:
            data = json.loads(request.body)

            bill = Bill.objects.create(
                customer_name=data.get("customer"),
                total_amount=float(data.get("total", 0))
            )

            for item in data.get("items", []):
                BillItem.objects.create(
                    bill=bill,
                    service_name=item.get("name", ""),
                    quantity=int(item.get("qty", 0)),
                    price=float(item.get("price", 0))
                )

            return JsonResponse({
                "status": "success",
                "invoice_no": bill.invoice_no
            })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })
    
# ✅ GENERATE INVOICE
def number_to_words(n):
    return num2words(n, to='cardinal', lang='en').title() + " Rupees Only"


# ✅ GENERATE INVOICE
def generate_invoice(request):

    data = json.loads(request.body)
    customer = data.get("customer")
    items = data.get("items")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4,
                            rightMargin=20, leftMargin=20,
                            topMargin=20, bottomMargin=20)

    styles = getSampleStyleSheet()
    elements = []

    # ===== FILE PATHS =====
    base = os.path.join(settings.BASE_DIR, "static/images")
    logo_path = os.path.join(base, "logo.png")
    stamp_path = os.path.join(base, "stamp.png")
    sign_path = os.path.join(base, "sign.png")

    # ===== HEADER =====
    logo = Image(logo_path, width=50, height=40) if os.path.exists(logo_path) else ""

    header = Table([
        [logo,
         Paragraph(
             "<b><font size=14>MEHER COMPUTING AND ONLINE</font></b><br/>"
             "Opp. Vasil-E-Najat, Badarpur<br/>"
             "Vadnagar, Mehsana, 384355<br/>"
             "<b>+91 97249 64906 / +91 97230 95530</b><br/>"
             "<font color='blue'>mehercomputing@gmail.com</font>",
             styles["Normal"]
         )]
    ], colWidths=[80, 400])

    elements.append(header)
    elements.append(Spacer(1, 10))

    # ===== TITLE =====
    elements.append(Table([["INVOICE"]], colWidths=[480], style=[
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#2f4f6f")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 14)
    ]))

    elements.append(Spacer(1, 15))

    # ===== INFO =====
    today = datetime.now().strftime("%d-%m-%Y")
    invoice_no = f"MEHER-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    info = Table([
        [
            Paragraph(f"<b>Customer Details</b><br/>{customer}", styles["Normal"]),
            Paragraph(f"<b>Bill To</b><br/>Invoice No: {invoice_no}<br/>Date: {today}", styles["Normal"])
        ]
    ], colWidths=[260, 260])

    info.setStyle([("BOX", (1, 0), (1, 0), 1, colors.black)])
    elements.append(info)
    elements.append(Spacer(1, 20))

    # ===== ITEMS =====
    table_data = [["SN", "Description", "Qty", "Price", "Amount"]]
    total = 0

    for i, item in enumerate(items, start=1):
        amt = float(item["qty"]) * float(item["price"])
        total += amt
        table_data.append([i, item["name"], item["qty"], item["price"], round(amt, 2)])

    table = Table(table_data, colWidths=[50, 220, 70, 80, 100])
    table.setStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ])

    elements.append(table)
    elements.append(Spacer(1, 20))

    # ===== TOTAL =====
    total_box = Table([
        ["Total Amount", f"₹ {total}"],
        ["Commission", ""],
        ["GST", ""],
        ["Grand Total", f"₹ {total}"]
    ], colWidths=[350, 150])

    total_box.setStyle([("GRID", (0, 0), (-1, -1), 1, colors.black)])
    elements.append(total_box)
    elements.append(Spacer(1, 20))

    # ===== AMOUNT IN WORDS =====
    words = num2words(total).title() + " Rupees Only"
    elements.append(Paragraph(f"<b>Amount in Words:</b> {words}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # ===== QR CODE =====
    qr_path = os.path.join(settings.BASE_DIR, "qr.png")
    qr = qrcode.make(f"Pay ₹{total} to Meher Computing")
    qr.save(qr_path)

    qr_img = Image(qr_path, width=80, height=80)

    # ===== SIGN + STAMP + QR =====
    sign = Image(sign_path, width=100, height=40) if os.path.exists(sign_path) else ""
    stamp = Image(stamp_path, width=100, height=80) if os.path.exists(stamp_path) else ""

    bottom = Table([
        [qr_img, stamp, sign],
        ["Scan to Pay", "Company Stamp", "Authorized Signature"]
    ], colWidths=[150, 150, 200])

    elements.append(bottom)
    elements.append(Spacer(1, 20))

    # ===== FOOTER =====
    elements.append(Paragraph(
        "<para align='center'><font color='red'><b>THANK YOU FOR YOUR BUSINESS</b></font></para>",
        styles["Normal"]
    ))

    doc.build(elements)
    return response


class BillHistoryView(ListView):
    model = Bill
    template_name = "bill_history.html"
    context_object_name = "bills"
    ordering = ['-date']



# ✅ PRINT INVOICE
def print_invoice(request, bill_id):

    bill = get_object_or_404(Bill, id=bill_id)
    items = bill.items.all()

    data = {
        "customer": bill.customer_name,
        "items": [
            {
                "name": i.service_name,
                "qty": i.quantity,
                "price": i.price
            } for i in items
        ]
    }

    # 🔥 existing PDF function reuse
    request._body = json.dumps(data).encode('utf-8')

    return generate_invoice(request)


