from django.contrib import admin
from .models import User, Professional, Patient, Appointment, Payment, ReviewRating, SubscriptionPlan, Admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'role', 'status')
    search_fields = ('full_name', 'email')

@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ('user', 'professional_code', 'consultation_fee', 'verify_status')
    list_filter = ('verify_status',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'patient_code', 'blood_group')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'professional', 'scheduled_at', 'appointment_status')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user_subscription', 'total_amount', 'payment_status')

# Register the rest
admin.site.register(ReviewRating)
admin.site.register(SubscriptionPlan)