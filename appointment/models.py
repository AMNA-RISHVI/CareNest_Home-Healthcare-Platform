from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class appointment(models.Model):
    appointment_id =models.AutoField(primary_key=True)
    patient=models.ForeignKey('patient_dashboard.Patient' ,
                               on_delete=models.CASCADE,
                          
                               )
    professional=models.ForeignKey('professionals.Professionals',
                                      on_delete=models.CASCADE,
                                   )
    #invoice=models.ForeignKey('invoice.invoice',
                                # on_delete=models.CASCADE,
                                 #)

    scheduled_at = models. DateTimeField()
    appointment_address = models.TextField()
    rescheduled_at=models.DateTimeField(null=True,blank=True)
    APPOINTMENT_STATUS=[('pending','pending'),
                        ( 'confirmed', 'confirmed'),
                        ('completed','completed'),
                        ('cancelled','cancelled'),
                        ( 'no-show', 'no-show'),
                        ( 'rescheduled','rescheduled'),
                        ]
    appointment_status= models.CharField(
                                max_length=20,
                                choices=APPOINTMENT_STATUS,
                                default='pending')
    patient_note=models.TextField(
        null=True,blank=True)

    def __str__(self):
        return (
            f"{self.patient} - "
            f"{self.professional} - "
            f"{self.scheduled_at}"
        )

    


class review_rating(models.Model):
    review_id = models.AutoField(primary_key=True)

    
   ### admin = models.ForeignKey(
   # 'admins.admin',
    #on_delete=models.SET_NULL,
    #null=True,
    #blank=True
   #)

    appointment = models.ForeignKey(
        'appointment.appointment',
        on_delete=models.CASCADE)

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField(
        null=True,
        blank=True
    )

    review_date = models.DateTimeField(
        auto_now_add=True
    )


    
    def __str__(self):
     return(
    f"{self.appointment.patient} - {self.appointment.professional} ({self.rating} stars)"
     )