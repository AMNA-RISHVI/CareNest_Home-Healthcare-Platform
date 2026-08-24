from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Patient, UserSubscription
from .forms import PatientForm
from .models import Patient
from .services import (
    can_add_family_member,
    get_active_subscription,
    get_family_member_count,
    get_family_member_limit,
)


@login_required
def dashboard(request):

    patients = Patient.objects.filter(
        user=request.user
    )

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

    context = {
        'patients': patients,
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



@login_required
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

    subscription = get_active_subscription(
        request.user
    )
        

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




@login_required
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




@login_required
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




@login_required
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