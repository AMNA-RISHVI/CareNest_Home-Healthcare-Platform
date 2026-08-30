from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from patient_dashboard.models import Patient


class Allergy(models.Model):

    SEVERITY_CHOICES = (
        ('Mild', 'Mild'),
        ('Moderate', 'Moderate'),
        ('Severe', 'Severe'),
    )

    allergy_id = models.BigAutoField(
        primary_key=True
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='health_wallet_allergies'
    )

    allergy_name = models.CharField(
        max_length=100
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='Mild'
    )

    reaction = models.CharField(
        max_length=255,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_health_wallet_allergies'
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_health_wallet_allergies'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.allergy_name} - "
            f"{self.patient.patient_name}"
        )


class ChronicCondition(models.Model):

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Managed', 'Managed'),
        ('Resolved', 'Resolved'),
    )

    condition_id = models.BigAutoField(
        primary_key=True
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='health_wallet_conditions'
    )

    condition_name = models.CharField(
        max_length=150
    )

    diagnosed_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active'
    )

    notes = models.TextField(
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_health_wallet_conditions'
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_health_wallet_conditions'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.condition_name} - "
            f"{self.patient.patient_name}"
        )


class Prescription(models.Model):

    prescription_id = models.BigAutoField(
        primary_key=True
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='health_wallet_prescriptions'
    )

    professional = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='health_wallet_prescriptions'
    )

    title = models.CharField(
        max_length=200
    )

    medication = models.CharField(
        max_length=255
    )

    dosage = models.TextField()

    instructions = models.TextField()

    prescription_date = models.DateField()

    prescription_file = models.FileField(
        upload_to='health_wallet/prescriptions/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'jpg',
                    'jpeg',
                    'png',
                    'pdf'
                ]
            )
        ]
    )

    notes = models.TextField(
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_health_wallet_prescriptions'
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_health_wallet_prescriptions'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.title} - "
            f"{self.patient.patient_name}"
        )


class LabReport(models.Model):

    report_id = models.BigAutoField(
        primary_key=True
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='health_wallet_lab_reports'
    )

    report_name = models.CharField(
        max_length=200
    )

    test_date = models.DateField()

    laboratory_name = models.CharField(
        max_length=200,
        blank=True
    )

    result_summary = models.TextField(
        blank=True
    )

    report_file = models.FileField(
        upload_to='health_wallet/lab_reports/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'jpg',
                    'jpeg',
                    'png',
                    'pdf'
                ]
            )
        ]
    )

    notes = models.TextField(
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_health_wallet_lab_reports'
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_health_wallet_lab_reports'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.report_name} - "
            f"{self.patient.patient_name}"
        )


class VaccinationRecord(models.Model):

    vaccination_id = models.BigAutoField(
        primary_key=True
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='health_wallet_vaccinations'
    )

    vaccine_name = models.CharField(
        max_length=150
    )

    vaccination_date = models.DateField()

    dose = models.CharField(
        max_length=50,
        blank=True
    )

    next_due_date = models.DateField(
        null=True,
        blank=True
    )

    provider = models.CharField(
        max_length=200,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_health_wallet_vaccinations'
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_health_wallet_vaccinations'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.vaccine_name} - "
            f"{self.patient.patient_name}"
        )


class MedicalHistory(models.Model):

    history_id = models.BigAutoField(
        primary_key=True
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='health_wallet_medical_history'
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    event_date = models.DateField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_health_wallet_history'
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_health_wallet_history'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.title} - "
            f"{self.patient.patient_name}"
        )


class ProfessionalPatientAccess(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('revoked', 'Revoked'),
        ('rejected', 'Rejected'),
    )

    access_id = models.BigAutoField(
        primary_key=True
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='professional_access'
    )

    professional = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_health_wallet_access'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    revoked_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "patient",
                    "professional"
                ],
                name="unique_patient_professional_access"
            )
        ]

    def __str__(self):
        return (
            f"{self.professional} → "
            f"{self.patient.patient_name} "
            f"({self.status})"
        )


class HealthRecordChange(models.Model):

    ACTION_CHOICES = (
        ('CREATE', 'Created'),
        ('UPDATE', 'Updated'),
        ('DELETE', 'Deleted'),
    )

    change_id = models.BigAutoField(
        primary_key=True
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='health_record_changes'
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='health_record_changes'
    )

    actor_role = models.CharField(
        max_length=30
    )

    category = models.CharField(
        max_length=50
    )

    record_id = models.PositiveBigIntegerField()

    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.actor} - "
            f"{self.action} - "
            f"{self.category}"
        )