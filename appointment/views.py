from django.shortcuts import render
from django.http import HttpResponse
from professionals.models import Professionals
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count

from professionals.models import (
    Professionals,
    ProfessionalsLocation,
    Specializations,
    Availability,
)
#from patients.models import Patient
from appointment.models import review_rating

# Create your views here
def appointment(request):
        
    professionals = Professionals.objects.all()
    return render(
        request,
        'appointment/appointment.html',
        {'professionals':professionals}
        )
def review_rate(request):
    return render(request,'appointment/review_rate.html')
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
        ).order_by('available_date', 'start_time')
    

    average_rating = rating_summary['average_rating']
    total_reviews = rating_summary['total_reviews']

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




