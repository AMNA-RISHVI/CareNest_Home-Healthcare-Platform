from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('professionals/', views.professionals_list, name='professionals'),
    path('patients/', views.patients_list, name='patients'),
    path('appointments/', views.appointments_list, name='appointments'),
    path('revenue/', views.revenue_analytics, name='revenue'),
    path('settings/', views.settings_page, name='settings'),
]