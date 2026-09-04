from django.db import migrations


def create_subscription_plans(apps, schema_editor):
    SubscriptionPlan = apps.get_model("subscriptions", "SubscriptionPlan")

    SubscriptionPlan.objects.get_or_create(
        plan_name="free plan",
        defaults={
            "price": 0,
            "duration_days": 30,
            "max_profile": 1,
            "description": "Perfect for individuals",
        },
    )

    SubscriptionPlan.objects.get_or_create(
        plan_name="family plan",
        defaults={
            "price": 3000,
            "duration_days": 30,
            "max_profile": 5,
            "description": "Best for families",
        },
    )

    SubscriptionPlan.objects.get_or_create(
        plan_name="senior care plan",
        defaults={
            "price": 2500,
            "duration_days": 30,
            "max_profile": 3,
            "description": "Elderly care focused",
        },
    )

    SubscriptionPlan.objects.get_or_create(
        plan_name="overseas parent care plan",
        defaults={
            "price": 3500,
            "duration_days": 30,
            "max_profile": 3,
            "description": "For expat families",
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_subscription_plans),
    ]
