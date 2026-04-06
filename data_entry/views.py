from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import DailyEntry
import json

class DataEntryView(TemplateView):
    template_name = "data_entry.html"

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            if data:
                selected_date = data[0].get('date')

                # 🔥 PURANA DATA DELETE
                DailyEntry.objects.filter(date=selected_date).delete()

            # 🔥 NAYA DATA SAVE
            for row in data:
                DailyEntry.objects.create(
                    date=row.get('date'),
                    xe=float(row.get('xe', 0) or 0),
                    press=float(row.get('press', 0) or 0),
                    online=float(row.get('online', 0) or 0),
                    color=float(row.get('color', 0) or 0),
                    xg=float(row.get('xg', 0) or 0),
                    pg=float(row.get('pg', 0) or 0),
                    og=float(row.get('og', 0) or 0),
                    cg=float(row.get('cg', 0) or 0),
                )

            return JsonResponse({"status": "success"}, status=201)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        
def fetch_data(request):
    date = request.GET.get('date')
    entries = DailyEntry.objects.filter(date=date).values()
    return JsonResponse({'data': list(entries)})