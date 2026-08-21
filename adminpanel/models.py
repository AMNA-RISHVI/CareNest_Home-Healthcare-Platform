from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('professional', 'Professional'),
        ('admin', 'Admin'),
    )
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    email_verify = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)
    status = models.BooleanField(default=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    district = models.CharField(max_length=20, blank=True)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_code = models.CharField(max_length=10, unique=True)
    post = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.user.full_name} - {self.post}"

class Professional(models.Model):
    VERIFY_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    professional_code = models.CharField(max_length=10, unique=True)
    nic_number = models.CharField(max_length=20, unique=True)
    qualifications = models.TextField()
    experience = models.CharField(max_length=255)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    language = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    verify_status = models.CharField(max_length=10, choices=VERIFY_STATUS, default='pending')
    verify_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.full_name

class Specialization(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)

class Availability(models.Model):
    DAYS_CHOICES = [(i, i) for i in range(7)]
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAYS_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

class ProfessionalsLocation(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = (
        ('free plan', 'Free Plan'),
        ('family plan', 'Family Plan'),
        ('senior care plan', 'Senior Care Plan'),
        ('overseas parent care plan', 'Overseas Parent Care Plan'),
    )
    plan_name = models.CharField(max_length=50, choices=PLAN_CHOICES, default='free plan')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField(default=30)
    max_profile = models.IntegerField(default=1)
    description = models.TextField(blank=True)

class UserSubscription(models.Model):
    STATUS_CHOICES = (
        ('activated', 'Activated'),
        ('deactivated', 'Deactivated'),
        ('expired', 'Expired'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    auto_renew = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activated')

class SubscriptionHistory(models.Model):
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    sub_date = models.DateTimeField(auto_now_add=True)

class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.SET_NULL, null=True)
    patient_code = models.CharField(max_length=10, unique=True)
    patient_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=20, blank=True)
    relationship = models.CharField(max_length=20, blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    notes = models.TextField()
    dosage = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    

class PatientDocument(models.Model):
    DOC_TYPES = (
        ('medical history', 'Medical History'),
        ('laboratory report', 'Lab Report'),
        ('diagnoses', 'Diagnoses'),
        ('vaccination', 'Vaccination'),
        ('treatment history', 'Treatment History'),
        ('prescriptions', 'Prescriptions'),
        ('allergies', 'Allergies'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prescription = models.ForeignKey(Prescription, on_delete=models.SET_NULL, null=True, blank=True)
    document_name = models.CharField(max_length=100)
    document_type = models.CharField(max_length=30, choices=DOC_TYPES, default='medical history')
    file_url = models.TextField(blank=True)
    uploaded_at = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

class Invoice(models.Model):
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    invoice_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=30, choices=[('card','Card'), ('online','Online'), ('bank_transfer','Bank Transfer')])
    transaction_id = models.CharField(max_length=20, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=[('pending','Pending'), ('completed','Completed'), ('failed','Failed'), ('refund','Refund')], default='pending')
    receipt_url = models.TextField(blank=True)

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), 
        ('cancelled', 'Cancelled'), ('denied', 'Denied'), ('no-show', 'No-Show')
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    scheduled_at = models.DateTimeField()
    appointment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rescheduled_at = models.DateTimeField(null=True, blank=True)
    patient_note = models.TextField(blank=True)

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, null=True, blank=True)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, null=True, blank=True)
    reminder_type = models.CharField(max_length=100)
    title = models.TextField()
    reminder_time = models.DateTimeField(auto_now_add=True)
    frequency = models.CharField(max_length=20, blank=True)

class ReviewRating(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i,i) for i in range(1,6)])
    review = models.TextField(blank=True)
    review_date = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    title = models.TextField()
    msg = models.TextField(blank=True)
    reference_id = models.IntegerField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)
    comments = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending','Pending'), ('viewed','Viewed'), ('resolved','Resolved')], default='pending')