from django.urls import path

from . import views


app_name = 'patient_dashboard'


urlpatterns = [

    path(
        '',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'family/add/',
        views.add_family_member,
        name='add_family_member'
    ),

    path(
        'family/<int:patient_id>/',
        views.patient_detail,
        name='patient_detail'
    ),

    path(
        'family/<int:patient_id>/edit/',
        views.edit_patient,
        name='edit_patient'
    ),

    path(
        'family/<int:patient_id>/delete/',
        views.delete_patient,
        name='delete_patient'
    ),

]