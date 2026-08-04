from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('PROFESSIONAL', 'Healthcare Professional'),
        ('ADMIN', 'Admin'),
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    SRI_LANKA_DISTRICTS = [
        ('Ampara', 'Ampara'),
        ('Anuradhapura', 'Anuradhapura'),
        ('Badulla', 'Badulla'),
        ('Batticaloa', 'Batticaloa'),
        ('Colombo', 'Colombo'),
        ('Galle', 'Galle'),
        ('Gampaha', 'Gampaha'),
        ('Hambantota', 'Hambantota'),
        ('Jaffna', 'Jaffna'),
        ('Kalutara', 'Kalutara'),
        ('Kandy', 'Kandy'),
        ('Kegalle', 'Kegalle'),
        ('Kilinochchi', 'Kilinochchi'),
        ('Kurunegala', 'Kurunegala'),
        ('Mannar', 'Mannar'),
        ('Matale', 'Matale'),
        ('Matara', 'Matara'),
        ('Monaragala', 'Monaragala'),
        ('Mullaitivu', 'Mullaitivu'),
        ('Nuwara Eliya', 'Nuwara Eliya'),
        ('Polonnaruwa', 'Polonnaruwa'),
        ('Puttalam', 'Puttalam'),
        ('Ratnapura', 'Ratnapura'),
        ('Trincomalee', 'Trincomalee'),
        ('Vavuniya', 'Vavuniya'),
    ]

    district = models.CharField(
        max_length=20,
        choices=SRI_LANKA_DISTRICTS,
        default='Colombo'
    )

    full_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    address = models.CharField(max_length=255)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='Male'
    )

    dob = models.DateField(
        blank=True,
        null=True
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    email_verified = models.BooleanField(
        default=False
    )

    status = models.BooleanField(
        default=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='PATIENT'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.username
    