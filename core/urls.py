"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dashboard.views import DashboardView
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponse

# 🚀 Fixed Admin Creator
def create_admin(request):
    # Username variable taaki dono jagah same rahe
    username = 'meher-online'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username, 
            email='mehercomputing@gmail.com', 
            password='Nepster#440'
        )
        return HttpResponse(f"✅ Success: Admin '{username}' created! Ab login kar sakte hain.")
    
    return HttpResponse(f"ℹ️ Info: Admin '{username}' pehle se bana hua hai.")

# 🔐 Root redirect (login ya dashboard)
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

urlpatterns = [
    # Pehle is path ko browser mein run karein: /make-me-admin/
    path('make-me-admin/', create_admin),

    # Admin Panel
    path('admin/', admin.site.urls),

    # Root Redirect
    path('', home_redirect),

    # Accounts (login/logout)
    path('', include('accounts.urls')),

    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Apps
    path('data/', include('data_entry.urls')),
    path('monthly/', include('monthly_summary.urls')),
    path('yearly/', include('yearly_summary.urls')),
    path('billing/', include('billing.urls')),
    path('expense/', include('expenses.urls')),
    path('udhaar/', include('udhaar.urls')),
]