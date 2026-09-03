from datetime import datetime

from django.db import transaction
from django.utils import timezone

from subscriptions.models import (
    SubscriptionPlan,
    UserSubscription,
    SubscriptionHistory,
)

from .models import Invoice, Payment


def generate_transaction_id():
    """
    Generate a simple fake transaction ID.
    """

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    return f'CN{timestamp}'


@transaction.atomic
def process_fake_payment(
    user_id,
    plan_id,
    payment_method
):
    """
    Process a fake subscription payment.

    This does NOT connect to a real payment gateway.
    It simply simulates a successful payment.
    """

    # Get the selected subscription plan
    plan = SubscriptionPlan.objects.get(
        plan_id=plan_id
    )

    # Create the subscription
    start_date = timezone.now().date()

    from datetime import timedelta

    due_date = start_date + timedelta(
        days=plan.duration_days
    )

    subscription = UserSubscription.objects.create(
        user_id=user_id,
        start_date=start_date,
        due_date=due_date,
        auto_renew=False,
        status='activated',
    )

    # Add subscription history
    SubscriptionHistory.objects.create(
        usersub=subscription,
        plan=plan,
    )

    # Create invoice
    invoice = Invoice.objects.create(
        usersub=subscription,
        created_at=start_date,
    )

    # Generate fake transaction ID
    transaction_id = generate_transaction_id()

    # Create payment record
    payment = Payment.objects.create(
        usersub=subscription,
        invoice=invoice,
        total_amount=plan.price,
        payment_method=payment_method,
        transaction_id=transaction_id,
        payment_date=timezone.now(),
        payment_status='completed',
    )

    return {
        'subscription': subscription,
        'invoice': invoice,
        'payment': payment,
    }