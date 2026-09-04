from django.db import models

# Create your models here.
class Professionals(models.Model):
    professional_id= models.AutoField(primary_key=True)
    User= models.OneToOneField('authentication.User', 
                            on_delete=models.CASCADE,
                           )
    service_type = models.CharField(
        max_length=20,
        choices=[
        ('doctor', 'Doctor Home Visit'),
        ('nursing', 'Nursing Care'),
        ('mlt', 'Medical Laboratory Technologist (MLT)'),
        ('physiotherapist', 'Physiotherapist'),
        ('caregiver', 'Caregiver'),
        ('nutritionist', 'Nutritionist'),
        ('counselor', 'Mental Health Counselor'),
        ]
    )
                            
    qualifications = models.TextField()
    qualifications_file = models.FileField(
        upload_to='qualifications/',
        null=True,
        blank=True
    )

    experience = models.TextField(max_length=255)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    language = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField( null=True)
    nic_number = models.CharField(unique=True, max_length=20)
    professional_code = models.CharField(unique=True, max_length=12)
    verify_status=[('pending','pending'),
	           ( 'approved','approved'),
	            ('rejected','rejected')]
    verify_status = models.CharField(
                             max_length=20,
                             choices=verify_status,
                             default='pending',

    )   
    #verify_by = models.ForeignKey(Admins,
                                 #on_delete=models.SET_NULL)

    def __str__(self):
        return self.professional_code

       
class Availability(models.Model):
    DAYS_CHOICES = [(i, i) for i in range(7)]
    availability_id = models.AutoField(primary_key=True)
    professional= models.ForeignKey('professionals.Professionals', 
                                     on_delete=models.CASCADE
                                    )
    available_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot = models.IntegerField()
    is_available = models.BooleanField(blank=True, null=True ,default=True)

    

class ProfessionalsLocation(models.Model):
    location_id = models.AutoField(primary_key=True)
    professional = models.ForeignKey(Professionals, 
                                     on_delete=models.CASCADE, )
    district = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    


class Specializations(models.Model):
    specialization_id = models.AutoField(primary_key=True)
    professional = models.ForeignKey(Professionals, 
                                     on_delete=models.CASCADE
                                     )
    description = models.CharField(max_length=100, blank=True, null=True)