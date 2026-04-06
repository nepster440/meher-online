from django.db import models

class DailyEntry(models.Model):
    date = models.DateField()

    xe = models.IntegerField(default=0)
    press = models.IntegerField(default=0)
    online = models.IntegerField(default=0)
    color = models.IntegerField(default=0)

    xg = models.IntegerField(default=0)
    pg = models.IntegerField(default=0)
    og = models.IntegerField(default=0)
    cg = models.IntegerField(default=0)

    def cash_total(self):
        return self.xe + self.press + self.online + self.color

    def gpay_total(self):
        return self.xg + self.pg + self.og + self.cg

    def grand_total(self):
        return self.cash_total() + self.gpay_total()

    def __str__(self):
        return f"{self.date} - {self.grand_total()}"