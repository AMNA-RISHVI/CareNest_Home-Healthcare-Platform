from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

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
    """
    Main patient dashboard.
    """

    patients = Patient.objects.filter(
        user=request.user
    ).order_by('patient_id')

    subscription = get_active_subscription(
        request.user
    )

    context = {
        'patients': patients,
        'subscription': subscription,
        'family_count': patients.count(),
        'family_limit': (
            subscription.plan.max_profile
            if subscription
            else 0
        ),
    }

    return render(
        request,
        'patient_dashboard/dashboard.html',
        context
    )


@login_required
def add_family_member(request):
    """
    Add a new family member/patient profile.
    """

    if not can_add_family_member(request.user):
        messages.error(
            request,
            'You have reached the maximum number '
            'of family profiles allowed by your subscription.'
        )

        return redirect('patient_dashboard:dashboard')

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

    else:
        form = PatientForm()

    subscription = get_active_subscription(
        request.user
    )

    context = {
        'form': form,
        'subscription': subscription,
        'family_count': get_family_member_count(
            request.user
        ),
        'family_limit': get_family_member_limit(
            request.user
        ),
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