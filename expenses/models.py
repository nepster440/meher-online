from django.db import models

class Expense(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=200)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"