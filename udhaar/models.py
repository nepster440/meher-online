from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Udhaar(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="entries")
    amount = models.FloatField()
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - ₹{self.amount}"


# 🔥 NEW MODEL (PAYMENT)
class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="payments")
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} Paid ₹{self.amount}"