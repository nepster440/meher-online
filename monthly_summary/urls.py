from django.urls import path
from .views import MonthlySummaryView
from .views import export_excel

urlpatterns = [
    path('', MonthlySummaryView.as_view(), name='monthly-summary'),
    path('export/', export_excel, name='export-excel'),
]