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
]