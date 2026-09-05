from django.shortcuts import render

from professionals.models import Professionals
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count
from patient_dashboard.models import Patient
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime,timedelta
from appointment.models import appointment, review_rating
from appointment.models import appointment
from patient_dashboard.models import Patient
from professionals.models import Availability

from professionals.models import (
    Professionals,
    ProfessionalsLocation,
    Specializations,
    Availability,
)
#from patients.models import Patient
from appointment.models import review_rating

# Create your views here
#appointment professional list
def appointment(request):
    patients = Patient.objects.filter(
        user=request.user
    ).order_by('patient_id')
        
    professionals = Professionals.objects.filter(verify_status="approved")
    
    selected_patient_id = request.GET.get('patient_id')
    selected_patient = None
    if selected_patient_id:
        selected_patient = get_object_or_404(
            Patient,
            patient_id=selected_patient_id,
            user=request.user
        )
    else:
        selected_patient = patients.first()

    return render(
        request,
        'appointment/find_professional.html',
        {
            'professionals': professionals,
            'patients': patients,
            'patient': selected_patient,
        }
    )

#review rating page
def review_rate(request):
    return render(request,'appointment/review_rate.html')

#appointment status
def appointment_status(request):
    return render(request,'appointment/appointment_status.html')


def book_appointment(request,professional_id):
    professional = get_object_or_404(
        Professionals,
        professional_id=professional_id
    )
   

    location = ProfessionalsLocation.objects.filter(
            professional=professional).first()

    specialization = Specializations.objects.filter(
            professional=professional).first()

        # Get reviews for this professional
    reviews = review_rating.objects.filter(
            appointment__professional=professional
        ).order_by('-review_id')

        # Calculate average rating
    rating_summary = reviews.aggregate(
            average_rating=Avg('rating'),
            total_reviews=Count('review_id')
        )
    availabilities = Availability.objects.filter(
            professional=professional,
            is_available=True
        ).order_by('day', 'start_time')
    

    average_rating = rating_summary['average_rating']
    total_reviews = rating_summary['total_reviews']

    #=======================handle book form

    if request.method == 'POST':

        selected_date = request.POST.get('selected_date')
        selected_time = request.POST.get('selected_time')
        address = request.POST.get('address')
        patient_note = request.POST.get('patient_note')

        if not selected_date or not selected_time:
            messages.error(
                request,
                'Please select a date and time.'
            )

            return redirect(
                'book_appointment',
                professional_id=professional_id
            )

        if not address:
            messages.error(
                request,
                'Please enter your address.'
            )

            return redirect(
                'book_appointment',
                professional_id=professional_id
            )
           # -----------------------------
        # Convert date and time
        # -----------------------------

        try:
            selected_datetime = datetime.strptime(
                f"{selected_date} {selected_time}",
                "%Y-%m-%d %H:%M"
            )

        except ValueError:
            messages.error(
                request,
                "Invalid date or time."
            )
            return redirect(
                "book_appointment",
                professional_id=professional_id
            )

        # Make timezone-aware
        selected_datetime = timezone.make_aware(
            selected_datetime
        )
          # Check date is not in the past
        # -----------------------------

        if selected_datetime <= timezone.now():

            messages.error(
                request,
                "Please select a future date and time."
            )



            return redirect(
                "book_appointment",
                professional_id=professional_id
            )

          # Check weekly availability
        # -----------------------------

        selected_day = selected_datetime.weekday()

        availability_exists = Availability.objects.filter(
            professional=professional,
            day=selected_day,
            is_available=True,
            start_time__lte=selected_datetime.time(),
            end_time__gt=selected_datetime.time()
        ).exists()

        if not availability_exists:

            messages.error(
                request,
                "The professional is not available at the selected time."
            )

            return redirect(
                "book_appointment",
                professional_id=professional_id

            )

        
        # Check whether slot is already booked
        # -----------------------------

        already_booked = appointment.objects.filter(
            professional=professional,
            scheduled_at=selected_datetime
        ).exclude(
            appointment_status__in=[
                "cancelled",
                "no-show"
            ]
        ).exists()

        if already_booked:

            messages.error(
                request,
                "This time slot is already booked."
            )

            return redirect(
                "book_appointment",
                professional_id=professional_id
            )
        
           # CREATE APPOINTMENT
        # -----------------------------

        new_appointment = appointment.objects.create(
            patient=patient,
            professional=professional,
            scheduled_at=selected_datetime,
            appointment_address=address,
            patient_note=patient_note,
            appointment_status="pending"
        )

        messages.success(
            request,
            "Appointment booked successfully."
        )

        return redirect(
            "appointment_status"
        )
    
    return render(
         request,
            'appointment/book_appointment.html',
        {
            'professional': professional,
            'location': location,
            'specialization': specialization,
            'reviews': reviews,
            'average_rating': average_rating,
            'total_reviews': total_reviews,
            'availabilities': availabilities,
            
        }
    )



    
def appointment_history(request):
    return render (request,'appointment/appointment_history.html')




