import uuid

from django.conf import settings
from django.db import models


class SubscriptionPlan(models.Model):

    plan_id = models.BigAutoField(
        primary_key=True
    )

    plan_name = models.CharField(
        max_length=50
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    duration_days = models.IntegerField(
        default=30
    )

    max_profile = models.PositiveIntegerField(
        default=1
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.plan_name


class UserSubscription(models.Model):

    STATUS_CHOICES = (
        ('activated', 'Activated'),
        ('deactivated', 'Deactivated'),
        ('expired', 'Expired'),
        ('pending', 'Pending'),
    )

    usersub_id = models.BigAutoField(
        primary_key=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name='user_subscriptions'
    )

    start_date = models.DateField(
        auto_now_add=True
    )

    due_date = models.DateField(
        null=True,
        blank=True
    )

    auto_renew = models.BooleanField(
        default=False
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='activated'
    )

    def __str__(self):
        return f"{self.user} - {self.plan}"


class Patient(models.Model):

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    RELATIONSHIP_CHOICES = (
        ('Self', 'Self'),
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Spouse', 'Spouse'),
        ('Son', 'Son'),
        ('Daughter', 'Daughter'),
        ('Brother', 'Brother'),
        ('Sister', 'Sister'),
        ('Grandfather', 'Grandfather'),
        ('Grandmother', 'Grandmother'),
        ('Other', 'Other'),
    )

    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )

    patient_id = models.BigAutoField(
        primary_key=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patients'
    )

    patient_code = models.CharField(
        max_length=10,
        unique=True,
        editable=False
    )

    patient_name = models.CharField(
        max_length=100
    )

    profile_picture = models.ImageField(
        upload_to='patient_profiles/',
        blank=True,
        null=True
    )

    relationship = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_CHOICES
    )

    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_CHOICES,
        blank=True
    )

    emergency_contact = models.CharField(
        max_length=20,
        blank=True
    )

    dob = models.DateField(
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.patient_code:
            self.patient_code = (
                f"P{uuid.uuid4().hex[:8].upper()}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient_name} ({self.relationship})"