from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import Expense
import json
from django.contrib.auth.mixins import LoginRequiredMixin

class ExpenseView(LoginRequiredMixin, TemplateView):
    template_name = "expense.html"

    def get(self, request, *args, **kwargs):

        # 👉 agar AJAX request hai to JSON bhejo
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            date = request.GET.get("date")

            if date:
                expenses = Expense.objects.filter(date=date)
            else:
                expenses = Expense.objects.all().order_by("-date")

            data = list(expenses.values())
            return JsonResponse({"data": data})

        # 👉 normal page load → HTML render karo
        return super().get(request, *args, **kwargs)

    def post(self, request):
        data = json.loads(request.body)

        Expense.objects.create(
            date=data.get("date"),
            title=data.get("title"),
            amount=float(data.get("amount"))
        )

        return JsonResponse({"status": "success"})

    def put(self, request):
        data = json.loads(request.body)

        exp = Expense.objects.get(id=data.get("id"))
        exp.title = data.get("title")
        exp.amount = float(data.get("amount"))
        exp.save()

        return JsonResponse({"status": "updated"})

    def delete(self, request):
        data = json.loads(request.body)

        Expense.objects.get(id=data.get("id")).delete()

        return JsonResponse({"status": "deleted"})