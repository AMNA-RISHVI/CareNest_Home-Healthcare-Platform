from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from appointment.models import review_rating
from django.shortcuts import get_object_or_404
from .forms import ProfessionalRegistrationForm
from django.contrib import messages
from django.http import JsonResponse
from professionals.models import Professionals, Availability
from django.views.decorators.http import require_POST
import uuid
from patient_dashboard.models import Patient
import json
from datetime import datetime



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


@login_required
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

        # Get patients belonging to logged-in user
    patients = Patient.objects.filter(
        user=request.user
    ).order_by('patient_id')

    # Get selected patient from URL
    selected_patient_id = request.GET.get('patient_id')

    if selected_patient_id:
        selected_patient = get_object_or_404(
            Patient,
            patient_id=selected_patient_id,
            user=request.user
        )
    else:
        selected_patient = patients.first()

    return render(request,'professionals/find_professional.html',
                  {
                    'professionals': professionals,
                    'patients': patients,
                    'patient': selected_patient,
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
# Appointments
    appointments = Appointment.objects.filter(professional=pro).exclude(appointment_status='completed').order_by('scheduled_at')
    appt_data = [{'id': a.appointment_id, 'patient': a.patient.patient_name, 'datetime': a.scheduled_at.strftime("%Y-%m-%d • %H:%M"), 'note': a.patient_note, 'status': a.appointment_status} for a in appointments]


#====================================================================================
# professional availability update
#===================================================================================
@login_required

#get page
def availability(request):
    if request.method =="GET":
        return render(
                request,
                "professionals/availability.html"
            )
    #save availability
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            schedule = data.get("schedule", {})


            professional = get_object_or_404(
                Professionals,
                User=request.user
            )

            Availability.objects.filter(
                professional=professional
            ).delete()
            for day, sessions in schedule.items():

                day_number = int(day)

                for session in sessions:

                    start_time = datetime.strptime(
                        session["start"],
                        "%H:%M"
                    ).time()

                    end_time = datetime.strptime(
                        session["end"],
                        "%H:%M"
                    ).time()

                    duration = 30

                    start_minutes = (
                        start_time.hour * 60 +
                        start_time.minute
                    )

                    end_minutes = (
                        end_time.hour * 60 +
                        end_time.minute
                    )

                    slot_count = (
                        end_minutes - start_minutes
                    ) // duration

                    if slot_count <= 0:
                        continue

                    session_type = (
                        "morning"
                        if start_time.hour < 12
                        else "afternoon"
                    )

                    Availability.objects.create(
                        professional=professional,
                        day=day_number,
                        session_type=session_type,
                        start_time=start_time,
                        end_time=end_time,
                        slot=slot_count,
                        is_available=True
                    )

                return JsonResponse({
                "success": True,
                "message": "Availability saved successfully."
                 })

        except Exception as e:

            return JsonResponse({
                    "success": False,
                    "message": str(e)
                }, status=400)
    return JsonResponse({
         "success": False,
         "message": "Invalid request method."
    }, status=400)

    






