from django.views.generic import TemplateView
from data_entry.models import DailyEntry
from django.db.models.functions import ExtractMonth
from django.db.models import Sum
from datetime import datetime
import calendar
from django.contrib.auth.mixins import LoginRequiredMixin

class YearlySummaryView(LoginRequiredMixin, TemplateView):
    template_name = "yearly_summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request
        year = int(request.GET.get("year", datetime.today().year))

        entries = DailyEntry.objects.filter(date__year=year)

        # Month-wise grouping
        monthly_data = {}

        for e in entries:
            m = e.date.month

            cash = e.xe + e.press + e.color
            gpay = e.online + e.xg + e.pg + e.og + e.cg

            if m not in monthly_data:
                monthly_data[m] = {"cash": 0, "gpay": 0}

            monthly_data[m]["cash"] += cash
            monthly_data[m]["gpay"] += gpay

        data = []
        total_cash = 0
        total_gpay = 0

        for i in range(1, 13):
            cash = monthly_data.get(i, {}).get("cash", 0)
            gpay = monthly_data.get(i, {}).get("gpay", 0)

            total_cash += cash
            total_gpay += gpay

            data.append({
                "month": calendar.month_name[i],
                "cash": cash,
                "gpay": gpay,
                "total": cash + gpay
            })

        context["data"] = data
        context["total_cash"] = total_cash
        context["total_gpay"] = total_gpay
        context["final_total"] = total_cash + total_gpay
        context["selected_year"] = year

        return context