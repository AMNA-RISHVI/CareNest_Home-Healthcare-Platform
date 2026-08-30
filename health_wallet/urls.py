from django.urls import path

from . import views


app_name = "health_wallet"


urlpatterns = [

    # ---------------------------------------------------------
    # MAIN HEALTH WALLET
    # ---------------------------------------------------------

    path(
        "",
        views.health_wallet,
        name="health_wallet"
    ),

    # ---------------------------------------------------------
    # ALL RECORDS
    # ---------------------------------------------------------

    path(
        "<int:patient_id>/records/",
        views.all_records,
        name="all_records"
    ),

    # ---------------------------------------------------------
    # ADD
    # ---------------------------------------------------------
    path(
        "<int:patient_id>/add/<str:category>/",
        views.add_record,
        name="add_record"
    ),

    

    # ---------------------------------------------------------
    # EDIT
    # ---------------------------------------------------------

    path(
        "<int:patient_id>/edit/<str:category>/<int:record_id>/",
        views.edit_record,
        name="edit_record"
    ),

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    path(
        "<int:patient_id>/delete/<str:category>/<int:record_id>/",
        views.delete_record,
        name="delete_record"
    ),


    path(
        "patient/<int:patient_id>/timeline/",
        views.health_timeline,
        name="health_timeline"
    ),

    path(
        "professional/request/<int:patient_id>/",
        views.request_patient_access,
        name="request_patient_access"
    ),

    path(
        "professional/request-access/",
        views.professional_request_access,
        name="professional_request_access"
    ),

    path(
        "professional/access/",
        views.professional_access_status,
        name="professional_access_status"
    ),

    path(
        "patient/access/",
        views.manage_professional_access,
        name="manage_professional_access"
    ),

    path(
        "patient/professional-access/<int:access_id>/approve/",
        views.approve_professional_access,
        name="approve_professional_access"
    ),

    path(
        "patient/professional-access/<int:access_id>/reject/",
        views.reject_professional_access,
        name="reject_professional_access"
    ),

    path(
        "patient/professional-access/<int:access_id>/revoke/",
        views.revoke_professional_access,
        name="revoke_professional_access"
    ),

    path(
        "professional/patient/<int:patient_id>/",
        views.professional_patient_records,
        name="professional_patient_records"
    ),

    path(
        "patient/<int:patient_id>/",
        views.health_wallet,
        name="health_wallet_patient"
    ),

    path(
        "<int:patient_id>/",
        views.health_wallet,
        name="health_wallet"
    ),

    path(
        "patient/<int:patient_id>/changes/",
        views.health_record_changes,
        name="health_record_changes"
    ),

 
]