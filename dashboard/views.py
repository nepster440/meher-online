from django.views.generic import TemplateView
from data_entry.models import DailyEntry
from datetime import date, timedelta
from expenses.models import Expense
import calendar

class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = date.today()

        # ===== FILTERS =====
        today_data = DailyEntry.objects.filter(date=today)
        monthly_data = DailyEntry.objects.filter(date__month=today.month, date__year=today.year)
        yearly_data = DailyEntry.objects.filter(date__year=today.year)

        expense_month = Expense.objects.filter(date__month=today.month, date__year=today.year)
        total_expense = sum([e.amount for e in expense_month])

        # ===== TOTAL INCOME =====
        today_income = sum([i.grand_total() for i in today_data])
        monthly_income = sum([i.grand_total() for i in monthly_data])
        yearly_income = sum([i.grand_total() for i in yearly_data])

        # ===== MONTH NAME =====
        month_name = calendar.month_name[today.month]

        # ===== BREAKDOWN (MONTH) =====
        xe = sum([i.xe for i in monthly_data])
        xg = sum([i.xg for i in monthly_data])

        press = sum([i.press for i in monthly_data])
        pg = sum([i.pg for i in monthly_data])

        online = sum([i.online for i in monthly_data])
        og = sum([i.og for i in monthly_data])

        color = sum([i.color for i in monthly_data])
        cg = sum([i.cg for i in monthly_data])

        # ===== YEARLY BREAKDOWN =====
        xe_y = sum([i.xe for i in yearly_data])
        xg_y = sum([i.xg for i in yearly_data])

        press_y = sum([i.press for i in yearly_data])
        pg_y = sum([i.pg for i in yearly_data])

        online_y = sum([i.online for i in yearly_data])
        og_y = sum([i.og for i in yearly_data])

        color_y = sum([i.color for i in yearly_data])
        cg_y = sum([i.cg for i in yearly_data])

        # ===== PROFIT =====
        profit = monthly_income - total_expense

        # ===== LAST 7 DAYS CHART =====
        last_7_days = []
        labels = []
        data = []

        for i in range(6, -1, -1):
            d = today - timedelta(days=i)
            day_data = DailyEntry.objects.filter(date=d)

            total = sum([x.grand_total() for x in day_data])

            labels.append(d.strftime("%d %b"))
            data.append(total)

        # ===== CONTEXT =====
        context.update({
            "today_income": today_income,
            "monthly_income": monthly_income,
            "yearly_income": yearly_income,
            "expense": total_expense,
            "profit": profit,

            "xe": xe + xg,
            "press": press + pg,
            "online": online + og,
            "color": color + cg,

            "xe_y": xe_y + xg_y,
            "press_y": press_y + pg_y,
            "online_y": online_y + og_y,
            "color_y": color_y + cg_y,

            "labels": labels,
            "data": data,
            "month_name": month_name,
            "year": today.year,
        })

        return context