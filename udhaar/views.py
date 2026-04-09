from django.shortcuts import get_object_or_404, render, redirect
from .models import Customer, Udhaar, Payment
from django.db.models import Sum

# Create your views here.
def udhaar_home(request):

    if request.method == "POST":

        action = request.POST.get("action")
        name = request.POST.get("customer")

        customer, _ = Customer.objects.get_or_create(name=name)

        # 👉 Udhaar add
        if action == "udhaar":
            amount = float(request.POST.get("amount"))
            desc = request.POST.get("desc")

            Udhaar.objects.create(
                customer=customer,
                amount=amount,
                description=desc
            )

        # 👉 Payment add
        elif action == "payment":
            amount = float(request.POST.get("amount"))

            Payment.objects.create(
                customer=customer,
                amount=amount
            )

        return redirect('udhaar')

    # ===== DISPLAY =====
    customers = Customer.objects.all()

    data = []

    for c in customers:

        total_udhaar = c.entries.aggregate(total=Sum('amount'))['total'] or 0
        total_paid = c.payments.aggregate(total=Sum('amount'))['total'] or 0

        balance = total_udhaar - total_paid

        data.append({
            "id": c.id,  # 👈 Yeh zaroori hai 'delete_customer' link ke liye
            "name": c.name,
            "udhaar": total_udhaar,
            "paid": total_paid,
            "balance": balance,
            "entries": c.entries.all(),  # ✅ Ye bilkul sahi hai
            "payments": c.payments.all()  # ✅ Ye bhi sahi hai
        })

    return render(request, "udhaar.html", {"data": data})



def delete_udhaar(request, id):
    entry = get_object_or_404(Udhaar, id=id)
    entry.delete()
    return redirect('udhaar')

def delete_payment(request, id):
    payment = get_object_or_404(Payment, id=id)
    payment.delete()
    return redirect('udhaar')

def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return redirect('udhaar')


def edit_udhaar(request, id):
    entry = get_object_or_404(Udhaar, id=id)

    if request.method == "POST":
        entry.amount = request.POST.get('amount')
        entry.description = request.POST.get('desc')
        entry.save()
        return redirect('udhaar')

    return render(request, 'edit_udhaar.html', {'entry': entry})



def delete_udhaar(request, id):
    entry = get_object_or_404(Udhaar, id=id)
    entry.delete()
    return redirect('udhaar')

def delete_payment(request, id):
    payment = get_object_or_404(Payment, id=id)
    payment.delete()
    return redirect('udhaar')

def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return redirect('udhaar')


def edit_udhaar(request, id):
    entry = get_object_or_404(Udhaar, id=id)

    if request.method == "POST":
        entry.amount = request.POST.get('amount')
        entry.description = request.POST.get('desc')
        entry.save()
        return redirect('udhaar')

    return render(request, 'edit_udhaar.html', {'entry': entry})