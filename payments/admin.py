from django.contrib import admin

from .models import Invoice, Payment


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_id',
        'usersub',
        'created_at',
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'payment_id',
        'usersub',
        'invoice',
        'total_amount',
        'payment_method',
        'transaction_id',
        'payment_date',
        'payment_status',
    )
