from django.urls import path
from .views import DataEntryView, fetch_data

urlpatterns = [
    # Main Data Entry Page
    path('', DataEntryView.as_view(), name='data_entry'),
    
    # AJAX Route: Date ke hisaab se data fetch karne ke liye
    path('fetch-data/', fetch_data, name='fetch-data'),
]