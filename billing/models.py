from django.db import models
from datetime import datetime

class Bill(models.Model):
    # Auto-generate Invoice Number: MEHER-YYYY-0001
    invoice_no = models.CharField(max_length=50, unique=True, null=True, blank=True)
    customer_name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    total_amount = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if not self.invoice_no:
            year = datetime.now().year
            last_bill = Bill.objects.filter(invoice_no__contains=f"MEHER-{year}").last()
            if last_bill:
                last_no = int(last_bill.invoice_no.split("-")[-1])
                new_no = str(last_no + 1).zfill(4)
            else:
                new_no = "0001"
            self.invoice_no = f"MEHER-{year}-{new_no}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_no} - {self.customer_name}"

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="items")
    service_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0)

    def total(self):
        return self.quantity * self.price