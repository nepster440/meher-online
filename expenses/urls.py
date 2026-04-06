from django.urls import path
from .views import ExpenseView

urlpatterns = [
    path('', ExpenseView.as_view(), name='expense'),
]