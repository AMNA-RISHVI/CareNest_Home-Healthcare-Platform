from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.payment_page,
        name='payment-page'
    ),

    path(
        'fake-payment/',
        views.fake_payment,
        name='fake-payment'
    ),

    path(
        'appointment/<int:appointment_id>/',
        views.appointment_payment,
        name='appointment-payment'
    ),
]