from django.shortcuts import render

from professionals.models import Professionals
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count
from patient_dashboard.models import Patient
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from appointment.models import appointment, review_rating


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
        
    professionals = Professionals.objects.filter(verify_status="approved")
    return render(
        request,
        'appointment/book_appointment.html',
        {'professionals':professionals}
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
    patient = get_object_or_404(
        Patient,
        user=request.user
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
        ).order_by('available_date', 'start_time')
    

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




