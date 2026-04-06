from django.db import models

# Create your models here.
class YearlySummary(models.Model):
    year = models.IntegerField()

    cash = models.FloatField(default=0)
    gpay = models.FloatField(default=0)

    expense = models.FloatField(default=0)

    def total(self):
        return self.cash + self.gpay

    def profit(self):
        return self.total() - self.expense