from django.db import models


class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('free plan', 'Free Plan'),
        ('family plan', 'Family Plan'),
        ('senior care plan', 'Senior Care Plan'),
        ('overseas parent care plan', 'Overseas Parent Care Plan'),
    ]

    plan_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(
        max_length=50,
        choices=PLAN_CHOICES,
        default='free plan'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    duration_days = models.IntegerField(default=30)
    max_profile = models.IntegerField(default=1)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'subscription_plan'

    def __str__(self):
        return self.get_plan_name_display()


class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('activated', 'Activated'),
        ('deactivated', 'Deactivated'),
        ('expired', 'Expired'),
        ('pending', 'Pending'),
    ]

    usersub_id = models.AutoField(primary_key=True)

    user_id = models.IntegerField()

    start_date = models.DateField(
        null=True,
        blank=True
    )
    due_date = models.DateField(
        null=True,
        blank=True
    )

    auto_renew = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='activated'
    )

    class Meta:
        db_table = 'user_subscription'

    def __str__(self):
        return f"Subscription {self.usersub_id}"


class SubscriptionHistory(models.Model):
    sub_historyid = models.AutoField(primary_key=True)

    usersub = models.ForeignKey(
        UserSubscription,
        on_delete=models.CASCADE,
        db_column='usersub_id',
        related_name='history'
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        db_column='plan_id',
        null=True,
        blank=True,
        related_name='subscription_history'
    )

    sub_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'subscription_history'

    def __str__(self):
        return f"History {self.sub_historyid}"
