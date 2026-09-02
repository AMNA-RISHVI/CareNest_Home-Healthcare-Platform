import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render

from .models import SubscriptionPlan
from .services import (
    purchase_subscription,
    get_current_subscription,
    get_subscription_history,
    renew_subscription,
    upgrade_subscription,
    downgrade_subscription,
)

def subscription_page(request):
    """Display the subscription plans page."""

    return render(
        request,
        'subscriptions/subscription.html'
    )
@require_GET
def subscription_plans(request):
    """Return all available subscription plans."""

    plans = SubscriptionPlan.objects.all()

    data = []

    for plan in plans:
        data.append({
            'plan_id': plan.plan_id,
            'plan_name': plan.get_plan_name_display(),
            'price': str(plan.price) if plan.price is not None else None,
            'duration_days': plan.duration_days,
            'max_profile': plan.max_profile,
            'description': plan.description,
        })

    return JsonResponse({
        'plans': data
    })


@require_GET
def current_subscription(request, user_id):
    """Return the user's current subscription."""

    subscription = get_current_subscription(user_id)

    if subscription is None:
        return JsonResponse({
            'message': 'No active subscription found.'
        }, status=404)

    latest_history = (
        subscription.history
        .order_by('-sub_date')
        .first()
    )

    plan = latest_history.plan if latest_history else None

    return JsonResponse({
        'usersub_id': subscription.usersub_id,
        'user_id': subscription.user_id,
        'plan': (
            plan.get_plan_name_display()
            if plan else None
        ),
        'start_date': subscription.start_date,
        'due_date': subscription.due_date,
        'auto_renew': subscription.auto_renew,
        'status': subscription.status,
    })


@require_POST
def purchase(request):
    """Purchase a subscription."""

    try:
        body = json.loads(request.body)

        user_id = body.get('user_id')
        plan_id = body.get('plan_id')

        if user_id is None or plan_id is None:
            return JsonResponse({
                'error': 'user_id and plan_id are required.'
            }, status=400)

        subscription = purchase_subscription(
            user_id=user_id,
            plan_id=plan_id
        )

        return JsonResponse({
            'message': 'Subscription purchased successfully.',
            'usersub_id': subscription.usersub_id,
            'status': subscription.status,
        }, status=201)

    except SubscriptionPlan.DoesNotExist:
        return JsonResponse({
            'error': 'Subscription plan not found.'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)


@require_POST
def renew(request, user_id):
    """Renew the user's subscription."""

    subscription = get_current_subscription(user_id)

    if subscription is None:
        return JsonResponse({
            'error': 'No active subscription found.'
        }, status=404)

    try:
        subscription = renew_subscription(subscription)

        return JsonResponse({
            'message': 'Subscription renewed successfully.',
            'usersub_id': subscription.usersub_id,
            'start_date': subscription.start_date,
            'due_date': subscription.due_date,
            'status': subscription.status,
        })

    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)


@require_POST
def upgrade(request, user_id):
    """Upgrade the user's subscription."""

    try:
        body = json.loads(request.body)

        new_plan_id = body.get('plan_id')

        if new_plan_id is None:
            return JsonResponse({
                'error': 'plan_id is required.'
            }, status=400)

        current = get_current_subscription(user_id)

        if current is None:
            return JsonResponse({
                'error': 'No active subscription found.'
            }, status=404)

        new_subscription = upgrade_subscription(
            subscription=current,
            new_plan_id=new_plan_id
        )

        return JsonResponse({
            'message': 'Subscription upgraded successfully.',
            'usersub_id': new_subscription.usersub_id,
            'status': new_subscription.status,
        })

    except SubscriptionPlan.DoesNotExist:
        return JsonResponse({
            'error': 'New subscription plan not found.'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)

@require_POST
def downgrade(request, user_id):
    """Downgrade the user's subscription."""

    try:
        body = json.loads(request.body)

        new_plan_id = body.get('plan_id')

        if new_plan_id is None:
            return JsonResponse({
                'error': 'plan_id is required.'
            }, status=400)

        current = get_current_subscription(user_id)

        if current is None:
            return JsonResponse({
                'error': 'No active subscription found.'
            }, status=404)

        new_subscription = downgrade_subscription(
            subscription=current,
            new_plan_id=new_plan_id
        )

        return JsonResponse({
            'message': 'Subscription downgraded successfully.',
            'usersub_id': new_subscription.usersub_id,
            'status': new_subscription.status,
        })

    except SubscriptionPlan.DoesNotExist:
        return JsonResponse({
            'error': 'New subscription plan not found.'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)


@require_GET
def subscription_history(request, user_id):
    """Return the user's subscription history."""

    history = get_subscription_history(user_id)

    data = []

    for record in history:
        data.append({
            'history_id': record.sub_historyid,
            'plan': (
                record.plan.get_plan_name_display()
                if record.plan else None
            ),
            'subscription_id': record.usersub.usersub_id,
            'date': record.sub_date,
        })

    return JsonResponse({
        'history': data
    })