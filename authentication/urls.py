from django.urls import path
from . import views

urlpatterns = [

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),

    path(
        "patient-dashboard/",
        views.patient_dashboard,
        name="patient_dashboard"
    ),

    path(
        "professional-dashboard/",
        views.professional_dashboard,
        name="professional_dashboard"
    ),

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "activate/<uidb64>/<token>/",
        views.activate,
        name="activate"
    ),

    path(
        "forgot-password/",
        views.forgot_password,
        name="forgot_password",
    ),

    path(
        "reset-password/<uidb64>/<token>/",
        views.reset_password,
        name="reset_password",
    ),

    path(
        "password-reset/done/",
        views.password_reset_done,
        name="password_reset_done",
    ),

    path(
        "verify-email/done/",
        views.verify_email_done,
        name="verify_email_done",
    ),

    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_profile"
    ),

    path(
        "change-password/",
        views.change_password,
        name="change_password"
    ),

]