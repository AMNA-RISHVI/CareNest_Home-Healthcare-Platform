from django.db import models

from subscriptions.models import UserSubscription


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)

    usersub = models.ForeignKey(
        UserSubscription,
        on_delete=models.CASCADE,
        db_column='usersub_id',
        related_name='invoices'
    )

    created_at = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'invoice'

    def __str__(self):
        return f"Invoice {self.invoice_id}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Card'),
        ('online', 'Online'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refund', 'Refund'),
    ]

    payment_id = models.AutoField(primary_key=True)

    usersub = models.ForeignKey(
        UserSubscription,
        on_delete=models.CASCADE,
        db_column='usersub_id',
        related_name='payments'
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        db_column='invoice_id',
        related_name='payments'
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES
    )

    transaction_id = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    payment_date = models.DateTimeField(
        null=True,
        blank=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )

    receipt_url = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'payment'

    def __str__(self):
        return f"Payment {self.payment_id}"