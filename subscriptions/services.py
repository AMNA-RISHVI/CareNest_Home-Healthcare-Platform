from datetime import timedelta

from django.utils import timezone

from .models import (
    SubscriptionPlan,
    UserSubscription,
    SubscriptionHistory,
)


def purchase_subscription(user_id, plan_id):
    """
    Create a new subscription for a user.
    """

    plan = SubscriptionPlan.objects.get(plan_id=plan_id)

    start_date = timezone.now().date()
    due_date = start_date + timedelta(days=plan.duration_days)

    subscription = UserSubscription.objects.create(
        user_id=user_id,
        start_date=start_date,
        due_date=due_date,
        auto_renew=False,
        status='activated',
    )

    SubscriptionHistory.objects.create(
        usersub=subscription,
        plan=plan,
    )

    return subscription


def get_user_profile_limit(user):
    subscription = get_current_subscription(user.id)

    if not subscription:
        return 1

    latest_history = (
        subscription.history
        .select_related('plan')
        .order_by('-sub_date')
        .first()
    )

    if not latest_history or not latest_history.plan:
        return 1

    return latest_history.plan.max_profile


def can_create_patient_profile(user, current_profile_count):
    max_profiles = get_user_profile_limit(user)

    return current_profile_count < max_profiles


def get_current_subscription(user_id):
    """
    Get the user's current active subscription.
    """

    return (
        UserSubscription.objects
        .filter(
            user_id=user_id,
            status='activated'
        )
        .order_by('-start_date')
        .first()
    )


def get_subscription_history(user_id):
    """
    Get all subscription history for a user.
    """

    subscriptions = UserSubscription.objects.filter(
        user_id=user_id
    )

    return (
        SubscriptionHistory.objects
        .filter(usersub__in=subscriptions)
        .order_by('-sub_date')
    )


def renew_subscription(subscription):
    """
    Renew an existing subscription.
    """

    latest_history = (
        SubscriptionHistory.objects
        .filter(usersub=subscription)
        .order_by('-sub_date')
        .first()
    )

    if latest_history is None:
        raise ValueError(
            'No subscription history found.'
        )

    plan = latest_history.plan

    if plan is None:
        raise ValueError(
            'No subscription plan found.'
        )

    subscription.start_date = subscription.due_date
    subscription.due_date = (
        subscription.start_date
        + timedelta(days=plan.duration_days)
    )
    subscription.status = 'activated'

    subscription.save()

    SubscriptionHistory.objects.create(
        usersub=subscription,
        plan=plan,
    )

    return subscription


def upgrade_subscription(subscription, new_plan_id):
    """
    Upgrade a user's subscription to a higher-priced plan.
    """

    new_plan = SubscriptionPlan.objects.get(
        plan_id=new_plan_id
    )

    latest_history = (
        SubscriptionHistory.objects
        .filter(usersub=subscription)
        .order_by('-sub_date')
        .first()
    )

    if latest_history is None or latest_history.plan is None:
        raise ValueError(
            'Current subscription plan not found.'
        )

    current_plan = latest_history.plan

    if new_plan.price <= current_plan.price:
        raise ValueError(
            'Selected plan is not an upgrade.'
        )

    # Deactivate the current subscription
    subscription.status = 'deactivated'
    subscription.save()

    # Create the new subscription
    start_date = timezone.now().date()
    due_date = start_date + timedelta(
        days=new_plan.duration_days
    )

    new_subscription = UserSubscription.objects.create(
        user_id=subscription.user_id,
        start_date=start_date,
        due_date=due_date,
        auto_renew=False,
        status='activated',
    )

    # Record the new plan in history
    SubscriptionHistory.objects.create(
        usersub=new_subscription,
        plan=new_plan,
    )

def downgrade_subscription(subscription, new_plan_id):
    """
    Downgrade a user's subscription to a lower-priced plan.
    """

    new_plan = SubscriptionPlan.objects.get(
        plan_id=new_plan_id
    )

    latest_history = (
        SubscriptionHistory.objects
        .filter(usersub=subscription)
        .order_by('-sub_date')
        .first()
    )

    if latest_history is None or latest_history.plan is None:
        raise ValueError(
            'Current subscription plan not found.'
        )

    current_plan = latest_history.plan

    if new_plan.price >= current_plan.price:
        raise ValueError(
            'Selected plan is not a downgrade.'
        )

    # Deactivate the current subscription
    subscription.status = 'deactivated'
    subscription.save()

    # Create the new subscription
    start_date = timezone.now().date()
    due_date = start_date + timedelta(
        days=new_plan.duration_days
    )

    new_subscription = UserSubscription.objects.create(
        user_id=subscription.user_id,
        start_date=start_date,
        due_date=due_date,
        auto_renew=False,
        status='activated',
    )

    # Record the new plan in history
    SubscriptionHistory.objects.create(
        usersub=new_subscription,
        plan=new_plan,
    )

def expire_subscriptions():
    """
    Mark active subscriptions as expired when their due date has passed.
    """

    today = timezone.now().date()

    expired_subscriptions = UserSubscription.objects.filter(
        status='activated',
        due_date__lt=today
    )

    count = expired_subscriptions.update(
        status='expired'
    )

    return count

    return new_subscription