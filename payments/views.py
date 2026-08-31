import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render

from subscriptions.models import SubscriptionPlan

from .services import process_fake_payment


def payment_page(request):
    return render(request, 'payments/payment.html')
@require_POST



def fake_payment(request):
    """
    Process a fake payment for a subscription.
    """

    try:
        body = json.loads(request.body)

        user_id = body.get('user_id')
        plan_id = body.get('plan_id')
        payment_method = body.get('payment_method')

        # Check required information
        if user_id is None:
            return JsonResponse({
                'error': 'user_id is required.'
            }, status=400)

        if plan_id is None:
            return JsonResponse({
                'error': 'plan_id is required.'
            }, status=400)

        if payment_method is None:
            return JsonResponse({
                'error': 'payment_method is required.'
            }, status=400)

        # Check that payment method is allowed
        allowed_methods = [
            'card',
            'online',
            'bank_transfer',
        ]

        if payment_method not in allowed_methods:
            return JsonResponse({
                'error': 'Invalid payment method.'
            }, status=400)

        # Process the fake payment
        result = process_fake_payment(
            user_id=user_id,
            plan_id=plan_id,
            payment_method=payment_method,
        )

        subscription = result['subscription']
        invoice = result['invoice']
        payment = result['payment']

        return JsonResponse({
            'message': 'Payment successful.',
            'subscription_id': subscription.usersub_id,
            'invoice_id': invoice.invoice_id,
            'payment_id': payment.payment_id,
            'transaction_id': payment.transaction_id,
            'amount': str(payment.total_amount),
            'payment_status': payment.payment_status,
        }, status=201)

    except SubscriptionPlan.DoesNotExist:
        return JsonResponse({
            'error': 'Subscription plan not found.'
        }, status=404)

    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data.'
        }, status=400)

    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)
