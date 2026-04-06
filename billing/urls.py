from django.urls import path
from .views import generate_invoice, BillingView, BillHistoryView, print_invoice

urlpatterns = [
    path('', BillingView.as_view(), name='billing'),
    path('save/', BillingView.as_view(), name='save_bill'),
    path('invoice/', generate_invoice, name='invoice'),
    path('history/', BillHistoryView.as_view(), name='bill_history'),

    # ✅ YE ADD KARNA HAI
    path('print/<int:bill_id>/', print_invoice, name='print_invoice'),
]