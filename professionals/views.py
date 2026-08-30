from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from appointment.models import review_rating

from .models import (
    Professionals,
    ProfessionalsLocation,
    Specializations,
 )

from appointment.models import review_rating


# Create your views here.
@login_required
def professionals(request):
    if request.method =='POST':
    

        #professional information
        qualifications=request.POST.get('qualifications')
        experience=request.POST.get('experience')
        consultation_fee = request.POST.get('consultation_fee')
        language = request.POST.get('language')
        bio = request.POST.get('bio')
        nic_number = request.POST.get('nic_number')
        professional_code = request.POST.get('professional_code')

        qualifications_file = request.FILES.get(
            'qualifications_file'
        )

        experience = request.POST.get('experience')
        consultation_fee = request.POST.get('consultation_fee')
        language = request.POST.get('language')
        bio = request.POST.get('bio')
        professional_code = request.POST.get('professional_code')

        qualifications_file = request.FILES.get(
            'qualifications_file'
        )

        # LOCATION DATA
        # -------------------------
        district = request.POST.get('district')
        city = request.POST.get('city')

           # SPECIALIZATION DATA
        # -------------------------
        specialization = request.POST.get('description')

        

        # 2. Create Professional profile
        Professionals.objects.create(
            User=request.user,
            qualifications=qualifications,
            qualifications_file=qualifications_file,
            experience=experience,
            consultation_fee=consultation_fee,
            language=language,
            bio=bio,
            professional_code=professional_code
        )

         # 3. CREATE LOCATION
        # -------------------------
        ProfessionalsLocation.objects.create(
            professional=professional,
            district=district,
            city=city
        )

         # 4. CREATE SPECIALIZATION
        # -------------------------
        Specializations.objects.create(
            professional=professional,
            description=specialization
        )



        return redirect('professional_profile')
     # Show registration page
    return render(
            request,
            'professionals/professional_regi.html'
    )

#=========================================
    # Professional Profile
#==========================================    
@login_required
def professional_profile(request):

    professional = Professionals.objects.get(
        User=request.user
    )

    location = ProfessionalsLocation.objects.filter(
        professional=professional
    ).first()

    specialization = Specializations.objects.filter(
        professional=professional
    ).first()



    return render(request,'professionals/professional_profile.html',
                   {
                        'professional': professional,
                        'location': location,
                        'specialization': specialization,
                     }
              )

        




def availability(request):
    return render(request,'professionals/availability.html')

def find_professional(request):
         # Get approved professionals
    professionals = Professionals.objects.filter(
        verify_status='approved'
    )

    # Get all reviews and calculate rating
    rating_data = review_rating.objects.values(
        'appointment__professional'
    ).annotate(
        average_rating=Avg('rating'),
        review_count=Count('review_id')
    )

     # Go through every professional
    for professional in professionals:

        professional.average_rating = None
        professional.total_reviews = 0

        # Find rating for this professional
        for data in rating_data:

            if data['appointment__professional'] == professional.professional_id:

                professional.average_rating = round(
                    data['average_rating'],
                    1
                )
                professional.total_reviews = data['review_count']

    return render(request,'professionals/find_professional.html',
                  {
                      'professionals': professionals 
                  }
                  )



def professional_dashboard(request):
    return render(request,'professionals/professional_dashboard.html')


