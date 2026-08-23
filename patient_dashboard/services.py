from .models import UserSubscription


def get_active_subscription(user):
    """
    Return the currently active subscription for a user.
    """

    return (
        UserSubscription.objects
        .select_related('plan')
        .filter(
            user=user,
            status='activated'
        )
        .order_by('-start_date')
        .first()
    )


def get_family_member_limit(user):
    """
    Return the maximum number of patient profiles
    allowed by the user's active subscription.
    """

    subscription = get_active_subscription(user)

    if not subscription:
        return 0

    return subscription.plan.max_profile


def get_family_member_count(user):
    """
    Return the current number of family members/patient
    profiles belonging to the user.
    """

    return user.patients.count()


def can_add_family_member(user):
    """
    Check whether the user can add another patient profile.
    """

    limit = get_family_member_limit(user)
    current_count = get_family_member_count(user)

    return current_count < limit