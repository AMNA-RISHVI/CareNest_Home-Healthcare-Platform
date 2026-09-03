from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.professional_dashboard, name='prof_dashboard'),
    path('get-data/', views.get_professional_data, name='get_prof_data'),
    path('availability-settings/', views.update_availability_page, name='availability_settings_page'),
    path('api/update-availability/', views.update_availability_api, name='update_availability_api'),
    path('update-appointment-status/', views.update_appointment_status, name='update_appointment_status'),
    path('save-settings/', views.save_settings, name='save_prof_settings'),
    path('upload-prescription/', views.upload_prescription, name='upload_prescription'),
    path('get-recent-prescriptions/', views.get_recent_prescriptions, name='get_recent_prescriptions'),
    path('view-prescription/<int:pk>/', views.view_prescription, name='view_prescription'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('prescriptions/', views.prescriptions_list, name='prescriptions'),
]