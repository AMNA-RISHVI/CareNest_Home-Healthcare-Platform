from django.urls import path

from . import views


urlpatterns = [

    path(
    '',
    views.subscription_page,
    name='subscription-page'
    ),
    path(
        'plans/',
        views.subscription_plans,
        name='subscription-plans'
    ),

    path(
        'current/<int:user_id>/',
        views.current_subscription,
        name='current-subscription'
    ),

    path(
        'purchase/',
        views.purchase,
        name='purchase-subscription'
    ),

    path(
        'renew/<int:user_id>/',
        views.renew,
        name='renew-subscription'
    ),

    path(
        'upgrade/<int:user_id>/',
        views.upgrade,
        name='upgrade-subscription'
    ),

    path(
    'downgrade/<int:user_id>/',
    views.downgrade,
    name='downgrade-subscription'
    ),

    path(
        'history/<int:user_id>/',
        views.subscription_history,
        name='subscription-history'
    ),
]