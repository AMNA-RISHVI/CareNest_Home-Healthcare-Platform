from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Patient, UserSubscription
from .forms import PatientForm
from .services import (
    can_add_family_member,
    get_active_subscription,
    get_family_member_count,
    get_family_member_limit,
)
from functools import wraps
from health_wallet.models import (
    Allergy,
    ChronicCondition,
    Prescription,
    LabReport,
    VaccinationRecord,
    MedicalHistory,
)



def patient_required(view_func):

    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):

        if request.user.role != "PATIENT":

            messages.error(
                request,
                "You do not have permission to access the patient dashboard."
            )

            # Send them back to an appropriate dashboard.
            if request.user.role == "ADMIN":
                return redirect("admin_dashboard")

            elif request.user.role == "PROFESSIONAL":
                return redirect("professional_dashboard")

            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper



@patient_required
def dashboard(request):

    patients = Patient.objects.filter(
        user=request.user
    ).order_by('patient_id')

    # =====================================================
    # HEALTH WALLET INFORMATION FOR EACH PATIENT
    # =====================================================

    for patient in patients:

        # -------------------------------------------------
        # ALLERGIES
        # -------------------------------------------------

        patient.dashboard_allergies = Allergy.objects.filter(
            patient=patient
        ).order_by("-created_at")


        # -------------------------------------------------
        # CHRONIC CONDITIONS
        # -------------------------------------------------

        patient.dashboard_conditions = ChronicCondition.objects.filter(
            patient=patient
        ).order_by("-created_at")


        # -------------------------------------------------
        # TOTAL HEALTH RECORDS
        #
        # Includes:
        # Allergies
        # Chronic Conditions
        # Prescriptions
        # Lab Reports
        # Vaccinations
        # Medical History
        # -------------------------------------------------

        patient.total_health_records = (
            patient.dashboard_allergies.count()
            + patient.dashboard_conditions.count()
            + Prescription.objects.filter(
                patient=patient
            ).count()
            + LabReport.objects.filter(
                patient=patient
            ).count()
            + VaccinationRecord.objects.filter(
                patient=patient
            ).count()
            + MedicalHistory.objects.filter(
                patient=patient
            ).count()
        )


        # -------------------------------------------------
        # ALLERGY INFORMATION
        # -------------------------------------------------

        patient.has_allergies = patient.dashboard_allergies.exists()

        patient.allergy_names = list(
            patient.dashboard_allergies.values_list(
                "allergy_name",
                flat=True
            )
        )


        # -------------------------------------------------
        # HEALTH STATUS
        # -------------------------------------------------

        if patient.dashboard_conditions.exists():

            patient.health_status = "Needs Attention"

        elif patient.dashboard_allergies.exists():

            patient.health_status = "Needs Attention"

        elif patient.total_health_records > 0:

            patient.health_status = "Good"

        else:

            patient.health_status = "No Data"


    subscription = get_active_subscription(
        request.user
    )

    max_profiles = get_family_member_limit(
        request.user
    )

    current_count = patients.count()

    can_add_family_member = (
        current_count < max_profiles
    )

    # ================================================
    # SELECTED PATIENT
    # ================================================

    selected_patient = patients.first()

    selected_patient_id = request.GET.get(
        'patient'
    )

    if selected_patient_id:

        try:

            selected_patient = patients.get(
                patient_id=selected_patient_id
            )

        except Patient.DoesNotExist:

            selected_patient = patients.first()

    context = {
        'patients': patients,
        'selected_patient': selected_patient,
        'subscription': subscription,
        'max_profiles': max_profiles,
        'current_count': current_count,
        'can_add_family_member': can_add_family_member,
    }

    return render(
        request,
        'patient_dashboard/dashboard.html',
        context
    )



@patient_required
def add_family_member(request):

    patients = Patient.objects.filter(
        user=request.user
    )

    current_count = patients.count()

    max_profiles = get_family_member_limit(
        request.user
    )


    # ================================================
    # CHECK SUBSCRIPTION LIMIT
    # ================================================

    if current_count >= max_profiles:

        messages.warning(
            request,
            "You have reached the maximum number of "
            "patient profiles allowed by your subscription."
        )

        return redirect(
            'patient_dashboard:dashboard'
        )


    # ================================================
    # FORM SUBMISSION
    # ================================================

    if request.method == 'POST':

        form = PatientForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            # Check again immediately before saving.
            if not can_add_family_member(request.user):
                messages.error(
                    request,
                    'You have reached your family profile limit.'
                )

                return redirect(
                    'patient_dashboard:dashboard'
                )

            patient = form.save(commit=False)

            patient.user = request.user

            patient.save()

    
            messages.success(
                request,
                'Family member added successfully.'
            )

            return redirect(
                'patient_dashboard:dashboard'
            )
        pass

    else:
        form = PatientForm()

        

    # ================================================
    # DISPLAY FORM
    # ================================================
    context = {
        'form': form,
        'max_profiles': max_profiles,
        'current_count': current_count,
    }

    return render(
        request,
        'patient_dashboard/add_family_member.html',
        context
    )



@patient_required
def patient_detail(request, patient_id):
    """
    Display a patient's profile.

    Only the account that owns the patient profile
    can access it.
    """

    patient = get_object_or_404(
        Patient,
        patient_id=patient_id,
        user=request.user
    )

    return render(
        request,
        'patient_dashboard/patient_detail.html',
        {
            'patient': patient
        }
    )




@patient_required
def edit_patient(request, patient_id):
    """
    Edit an existing family member.
    """

    patient = get_object_or_404(
        Patient,
        patient_id=patient_id,
        user=request.user
    )

    if request.method == 'POST':

        form = PatientForm(
            request.POST,
            request.FILES,
            instance=patient
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Family member updated successfully.'
            )

            return redirect(
                'patient_dashboard:patient_detail',
                patient_id=patient.patient_id
            )

    else:

        form = PatientForm(
            instance=patient
        )

    return render(
        request,
        'patient_dashboard/edit_patient.html',
        {
            'form': form,
            'patient': patient
        }
    )




@patient_required
def delete_patient(request, patient_id):
    """
    Delete a family member.
    """

    patient = get_object_or_404(
        Patient,
        patient_id=patient_id,
        user=request.user
    )

    if request.method == 'POST':

        patient_name = patient.patient_name

        patient.delete()

        messages.success(
            request,
            f'{patient_name} was removed successfully.'
        )

        return redirect(
            'patient_dashboard:dashboard'
        )

    return render(
        request,
        'patient_dashboard/delete_patient.html',
        {
            'patient': patient
        }
    )


def get_active_subscription(user):

    return UserSubscription.objects.filter(
        user=user,
        status='activated'
    ).select_related(
        'plan'
    ).first()

def get_family_member_limit(user):

    subscription = get_active_subscription(user)

    if not subscription:
        return 1

    return subscription.plan.max_profile