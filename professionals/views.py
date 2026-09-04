from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from appointment.models import review_rating
from django.shortcuts import get_object_or_404
from .forms import ProfessionalRegistrationForm
from django.contrib import messages
import uuid



from .models import (
    Professionals,
    ProfessionalsLocation,
    Specializations,
 )

from appointment.models import review_rating


# Create your views here.
##================regiser===================
@login_required
def professional_register(request):
    # only professionals can access this page
    if request.user.role != "PROFESSIONAL":
        return redirect("login")

    #Check whether professional profile already exists
    if Professionals.objects.filter(User=request.user).exists():
        return redirect("professionals:professional_dashboard")


    if request.method == "POST":

        form = ProfessionalRegistrationForm(
            request.POST,
            request.FILES
        )
        qualification_list = request.POST.getlist("qualification")

        qualification_text = "\n".join(
            q.strip()
            for q in qualification_list
            if q.strip()
        )

        if form.is_valid():

            professional = form.save(commit=False)

            professional.User = request.user
            professional.verify_status = "pending"
            professional.professional_code = f"PRO-{uuid.uuid4().hex[:8].upper()}"

            professional.save()


            #2. save location
            ProfessionalsLocation.objects.create(
                professional=professional,
                district=form.cleaned_data["district"],
                city=form.cleaned_data["city"]
            )

            #3. save speacialization
            
            specializations = request.POST.getlist("description")

            for specialization in specializations:

                specialization = specialization.strip()

                if specialization:
                    Specializations.objects.create(
                        professional=professional,
                        description=specialization
                    )


            messages.success(
                request,
                "Professional registration completed successfully."
            )

            return redirect("professional_dashboard")

    else:

        form = ProfessionalRegistrationForm()

    return render(
        request,
        "professionals/professional_register.html",
        {
            "form": form
        }
    )

   

#=========================================
    # Professional Profile
#==========================================    
@login_required
def professional_profile(request):

    professional = get_object_or_404(
        Professionals,
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



#=================================================================
# find professionals
# ========================================        



def find_professional(request):
         # Get approved professionals
    professionals = Professionals.objects.all(
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



#==========================================================
#professional dashboard
#========================================
@login_required
def professional_dashboard(request):

    professional = get_object_or_404(
        Professionals,
        User=request.user
    )

    return render(
        request,
        "professionals/professional_dashboard.html",
        {
            "professional": professional
        }
    )







