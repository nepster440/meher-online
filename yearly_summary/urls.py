from django.urls import path
from .views import YearlySummaryView

urlpatterns = [
    path('', YearlySummaryView.as_view(), name='yearly-summary'),
]