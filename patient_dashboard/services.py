from subscriptions.services import (
    get_current_subscription,
    get_user_profile_limit,
    can_create_patient_profile,
)
from subscriptions.models import UserSubscription

def get_active_subscription(user):
    """
    Return the currently active subscription for a user.
    """

    return (
        UserSubscription.objects
        .filter(
            user_id=user.id,
            status='activated'
        )
        .order_by('-start_date')
        .first()
    )


def get_family_member_limit(user):
    return get_user_profile_limit(user)


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

