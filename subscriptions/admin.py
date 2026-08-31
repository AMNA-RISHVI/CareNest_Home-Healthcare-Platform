from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription, SubscriptionHistory


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        'plan_id',
        'plan_name',
        'price',
        'duration_days',
        'max_profile',
    )


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'usersub_id',
        'user_id',
        'start_date',
        'due_date',
        'auto_renew',
        'status',
    )


@admin.register(SubscriptionHistory)
class SubscriptionHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'sub_historyid',
        'usersub',
        'plan',
        'sub_date',
    )
