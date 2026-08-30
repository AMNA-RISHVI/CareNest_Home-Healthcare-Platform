from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from patient_dashboard.models import Patient

from .models import (
    Allergy,
    ChronicCondition,
    Prescription,
    LabReport,
    VaccinationRecord,
    MedicalHistory,
)

from .services import (
    can_access_patient_records,
    can_modify_patient_records,
    create_health_record_change,
    professional_has_access,
)

from django.contrib import messages
from django.utils import timezone

from .models import ProfessionalPatientAccess



def get_record_model(category):
    """
    Return model and primary-key field for a health record category.
    """

    record_map = {

        "allergies": (
            Allergy,
            "allergy_id"
        ),

        "chronic_conditions": (
            ChronicCondition,
            "condition_id"
        ),

        "prescriptions": (
            Prescription,
            "prescription_id"
        ),

        "lab_reports": (
            LabReport,
            "report_id"
        ),

        "vaccinations": (
            VaccinationRecord,
            "vaccination_id"
        ),

        "medical_history": (
            MedicalHistory,
            "history_id"
        ),
    }

    return record_map.get(category)



def get_record_form(category):
    """
    Return the correct ModelForm for a category.
    """

    from .forms import (
        AllergyForm,
        ChronicConditionForm,
        PrescriptionForm,
        LabReportForm,
        VaccinationRecordForm,
        MedicalHistoryForm,
    )

    form_map = {

        "allergies": AllergyForm,

        "chronic_conditions": ChronicConditionForm,

        "prescriptions": PrescriptionForm,

        "lab_reports": LabReportForm,

        "vaccinations": VaccinationRecordForm,

        "medical_history": MedicalHistoryForm,
    }

    return form_map.get(category)



@login_required
def health_wallet(request, patient_id=None):

    if getattr(request.user, "role", None) != "PATIENT":
        raise PermissionDenied(
            "Only patient users can access the Health Wallet."
        )

    patients = Patient.objects.filter(
        user=request.user
    ).order_by("patient_id")

    if not patients.exists():
        return render(
            request,
            "health_wallet/health_wallet.html",
            {
                "patients": patients,
                "selected_patient": None,
                "allergies": [],
                "conditions": [],
                "prescriptions": [],
                "lab_reports": [],
                "vaccinations": [],
            }
        )

    # ---------------------------------------------------------
    # SELECT FAMILY MEMBER
    # ---------------------------------------------------------

    if patient_id:

        selected_patient = get_object_or_404(
            patients,
            patient_id=patient_id
        )

    else:

        selected_patient = patients.first()

    # ---------------------------------------------------------
    # LATEST RECORDS
    # ---------------------------------------------------------

    latest_allergy = Allergy.objects.filter(
        patient=selected_patient
    ).order_by(
        "-created_at"
    ).first()

    latest_condition = ChronicCondition.objects.filter(
        patient=selected_patient
    ).order_by(
        "-created_at"
    ).first()

    latest_prescription = Prescription.objects.filter(
        patient=selected_patient
    ).order_by(
        "-prescription_date",
        "-created_at"
    ).first()

    latest_lab_report = LabReport.objects.filter(
        patient=selected_patient
    ).order_by(
        "-test_date",
        "-created_at"
    ).first()

    latest_vaccination = VaccinationRecord.objects.filter(
        patient=selected_patient
    ).order_by(
        "-vaccination_date",
        "-created_at"
    ).first()

    context = {

        "patients": patients,

        "selected_patient": selected_patient,

        "latest_allergy": latest_allergy,

        "latest_condition": latest_condition,

        "latest_prescription": latest_prescription,

        "latest_lab_report": latest_lab_report,

        "latest_vaccination": latest_vaccination,
    }

    return render(
        request,
        "health_wallet/health_wallet.html",
        context
    )



@login_required
def all_records(request, patient_id):

    patient = get_object_or_404(
        Patient,
        patient_id=patient_id
    )

    # =========================================================
    # SECURITY
    # =========================================================

    # Patient owner OR approved professional
    if not can_access_patient_records(
        request.user,
        patient
    ):
        raise PermissionDenied(
            "You do not have permission to access this patient's health records."
        )

    # =========================================================
    # CATEGORY FILTER
    # =========================================================

    category = request.GET.get(
        "category",
        "all"
    )

    allowed_categories = [
        "all",
        "allergies",
        "chronic",
        "prescriptions",
        "lab_reports",
        "vaccination",
        "medical_history",
    ]

    if category not in allowed_categories:
        category = "all"

    # =========================================================
    # RECORD DATA
    # =========================================================

    allergies = Allergy.objects.filter(
        patient=patient
    ).order_by(
        "-created_at"
    )

    chronic_conditions = ChronicCondition.objects.filter(
        patient=patient
    ).order_by(
        "-created_at"
    )

    prescriptions = Prescription.objects.filter(
        patient=patient
    ).order_by(
        "-prescription_date",
        "-created_at"
    )

    lab_reports = LabReport.objects.filter(
        patient=patient
    ).order_by(
        "-test_date",
        "-created_at"
    )

    vaccinations = VaccinationRecord.objects.filter(
        patient=patient
    ).order_by(
        "-vaccination_date",
        "-created_at"
    )

    # Medical History is a separate filter.
    # It must NOT appear when category="all".
    medical_history = MedicalHistory.objects.filter(
        patient=patient
    ).order_by(
        "-event_date",
        "-created_at"
    )

    # =========================================================
    # DETERMINE USER AUTHORITY
    # =========================================================

    is_patient_owner = (
        request.user.role == "PATIENT"
        and patient.user_id == request.user.id
    )

    is_connected_professional = (
        request.user.role == "PROFESSIONAL"
        and professional_has_access(
            request.user,
            patient
        )
    )

    # =========================================================
    # CONTEXT
    # =========================================================

    context = {

        "patient": patient,

        "category": category,

        "allergies": allergies,

        "chronic_conditions": chronic_conditions,

        "prescriptions": prescriptions,

        "lab_reports": lab_reports,

        "vaccinations": vaccinations,

        "medical_history": medical_history,

        # Useful for template permission controls
        "is_patient_owner": is_patient_owner,

        "is_connected_professional": is_connected_professional,

        # Both can currently modify records
        "can_modify_records": can_modify_patient_records(
            request.user,
            patient
        ),
    }

    return render(
        request,
        "health_wallet/all_records.html",
        context
    )





@login_required
def add_record(request, patient_id, category):

    patient = get_object_or_404(
        Patient,
        patient_id=patient_id
    )

    # ---------------------------------------------------------
    # SECURITY
    # ---------------------------------------------------------

    if not can_modify_patient_records(
        request.user,
        patient
    ):
        raise PermissionDenied(
            "You do not have permission to add health records."
        )

    FormClass = get_record_form(category)

    if FormClass is None:
        raise PermissionDenied(
            "Invalid health record category."
        )

    # ---------------------------------------------------------
    # SUBMIT
    # ---------------------------------------------------------

    if request.method == "POST":

        form = FormClass(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            record = form.save(
                commit=False
            )

            record.patient = patient

            record.created_by = request.user

            record.updated_by = request.user

            # Prescription-specific field
            if isinstance(record, Prescription):

                if getattr(
                    request.user,
                    "role",
                    None
                ) == "PROFESSIONAL":

                    record.professional = request.user

            record.save()

            # -------------------------------------------------
            # AUDIT
            # -------------------------------------------------

            primary_key = record.pk

            create_health_record_change(

                patient=patient,

                actor=request.user,

                category=category,

                record_id=primary_key,

                action="CREATE",

                description=(
                    f"{category.replace('_', ' ').title()} "
                    f"record created by "
                    f"{getattr(request.user, 'role', 'user')}."
                )
            )

            return redirect(
                "health_wallet:all_records",
                patient_id=patient.patient_id
            )

    else:

        form = FormClass()

    return render(
        request,
        "health_wallet/add_record.html",
        {
            "form": form,
            "patient": patient,
            "category": category,
            "mode": "add",
        }
    )




@login_required
def edit_record(
    request,
    patient_id,
    category,
    record_id
):

    patient = get_object_or_404(
        Patient,
        patient_id=patient_id
    )

    # ---------------------------------------------------------
    # SECURITY
    # ---------------------------------------------------------

    if not can_modify_patient_records(
        request.user,
        patient
    ):
        raise PermissionDenied(
            "You do not have permission to edit this record."
        )

    record_info = get_record_model(
        category
    )

    if record_info is None:
        raise PermissionDenied(
            "Invalid health record category."
        )

    ModelClass, pk_field = record_info

    record = get_object_or_404(
        ModelClass,
        **{
            pk_field: record_id,
            "patient": patient
        }
    )

    FormClass = get_record_form(
        category
    )

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    if request.method == "POST":

        form = FormClass(
            request.POST,
            request.FILES,
            instance=record
        )

        if form.is_valid():

            updated_record = form.save(
                commit=False
            )

            updated_record.updated_by = (
                request.user
            )

            if isinstance(updated_record, Prescription):

                if getattr(
                    request.user,
                    "role",
                    None
                ) == "PROFESSIONAL":

                    updated_record.professional = request.user

            updated_record.save()


            # -------------------------------------------------
            # AUDIT
            # -------------------------------------------------

            create_health_record_change(

                patient=patient,

                actor=request.user,

                category=category,

                record_id=record.pk,

                action="UPDATE",

                description=(
                    f"{category.replace('_', ' ').title()} "
                    f"record updated by "
                    f"{getattr(request.user, 'role', 'user')}."
                )
            )

            return redirect(
                "health_wallet:all_records",
                patient_id=patient.patient_id
            )

    else:

        form = FormClass(
            instance=record
        )

    return render(
        request,
        "health_wallet/edit_record.html",
        {
            "form": form,
            "patient": patient,
            "category": category,
            "record": record,
            "mode": "edit",
        }
    )





@login_required
def delete_record(
    request,
    patient_id,
    category,
    record_id
):

    patient = get_object_or_404(
        Patient,
        patient_id=patient_id
    )

    # ---------------------------------------------------------
    # SECURITY
    # ---------------------------------------------------------

    if not can_modify_patient_records(
        request.user,
        patient
    ):
        raise PermissionDenied(
            "You do not have permission to delete this record."
        )

    record_info = get_record_model(
        category
    )

    if record_info is None:
        raise PermissionDenied(
            "Invalid health record category."
        )

    ModelClass, pk_field = record_info

    record = get_object_or_404(
        ModelClass,
        **{
            pk_field: record_id,
            "patient": patient
        }
    )

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    if request.method == "POST":

        # Store ID before deletion
        deleted_record_id = record.pk

        record.delete()

        # -----------------------------------------------------
        # AUDIT
        # -----------------------------------------------------

        create_health_record_change(

            patient=patient,

            actor=request.user,

            category=category,

            record_id=deleted_record_id,

            action="DELETE",

            description=(
                f"{category.replace('_', ' ').title()} "
                f"record deleted by "
                f"{getattr(request.user, 'role', 'user')}."
            )
        )

        return redirect(
            "health_wallet:all_records",
            patient_id=patient.patient_id
        )

    # ---------------------------------------------------------
    # CONFIRMATION
    # ---------------------------------------------------------

    return render(
        request,
        "health_wallet/delete_record.html",
        {
            "patient": patient,
            "record": record,
            "category": category,
        }
    )




@login_required
def health_timeline(request, patient_id):

    patient = get_object_or_404(
        Patient,
        patient_id=patient_id
    )

    # ---------------------------------------------------------
    # SECURITY
    # ---------------------------------------------------------

    if not can_access_patient_records(
        request.user,
        patient
    ):
        raise PermissionDenied(
            "You do not have permission to view this timeline."
        )

    # ---------------------------------------------------------
    # GET ALL RECORDS
    # ---------------------------------------------------------

    allergies = Allergy.objects.filter(
        patient=patient
    )

    chronic_conditions = ChronicCondition.objects.filter(
        patient=patient
    )

    prescriptions = Prescription.objects.filter(
        patient=patient
    )

    lab_reports = LabReport.objects.filter(
        patient=patient
    )

    vaccinations = VaccinationRecord.objects.filter(
        patient=patient
    )

    medical_history = MedicalHistory.objects.filter(
        patient=patient
    )

    # ---------------------------------------------------------
    # BUILD TIMELINE
    # ---------------------------------------------------------

    timeline = []

    for record in allergies:

        timeline.append({
            "date": record.created_at.date(),
            "category": "Allergy",
            "title": record.allergy_name,
            "record": record,
        })

    for record in chronic_conditions:

        timeline.append({
            "date": record.diagnosed_date or record.created_at.date(),
            "category": "Chronic Condition",
            "title": record.condition_name,
            "record": record,
        })

    for record in prescriptions:

        timeline.append({
            "date": record.prescription_date,
            "category": "Prescription",
            "title": record.title,
            "record": record,
        })

    for record in lab_reports:

        timeline.append({
            "date": record.test_date,
            "category": "Laboratory Report",
            "title": record.report_name,
            "record": record,
        })

    for record in vaccinations:

        timeline.append({
            "date": record.vaccination_date,
            "category": "Vaccination",
            "title": record.vaccine_name,
            "record": record,
        })

    for record in medical_history:

        timeline.append({
            "date": record.event_date,
            "category": "Medical History",
            "title": record.title,
            "record": record,
        })

    # Latest first
    timeline.sort(
        key=lambda item: item["date"],
        reverse=True
    )

    return render(
        request,
        "health_wallet/health_timeline.html",
        {
            "patient": patient,
            "timeline": timeline,
        }
    )



@login_required
def request_patient_access(request, patient_id):
    """
    Allow a healthcare professional to request access
    to a patient's health wallet.
    """

    if getattr(request.user, "role", None) != "PROFESSIONAL":
        raise PermissionDenied(
            "Only healthcare professionals can request patient access."
        )

    if request.method != "POST":
        return redirect(
            "health_wallet:professional_request_access"
        )

    patient = get_object_or_404(
        Patient,
        patient_id=patient_id
    )

    existing_access = ProfessionalPatientAccess.objects.filter(
        patient=patient,
        professional=request.user
    ).first()

    # ---------------------------------------------------------
    # ALREADY ACTIVE
    # ---------------------------------------------------------

    if existing_access:

        if existing_access.status == "active":

            messages.info(
                request,
                "You already have active access to this patient's health wallet."
            )

            return redirect(
                "health_wallet:professional_access_status"
            )

        # -----------------------------------------------------
        # ALREADY PENDING
        # -----------------------------------------------------

        if existing_access.status == "pending":

            messages.info(
                request,
                "Your access request is already pending patient approval."
            )

            return redirect(
                "health_wallet:professional_access_status"
            )

        # -----------------------------------------------------
        # REJECTED / REVOKED
        # -----------------------------------------------------
        # Allow the professional to request access again.

        existing_access.status = "pending"
        existing_access.requested_at = timezone.now()
        existing_access.approved_at = None
        existing_access.revoked_at = None

        existing_access.save(
            update_fields=[
                "status",
                "requested_at",
                "approved_at",
                "revoked_at",
            ]
        )

        messages.success(
            request,
            "A new access request has been sent to the patient."
        )

        return redirect(
            "health_wallet:professional_access_status"
        )

    # ---------------------------------------------------------
    # CREATE NEW REQUEST
    # ---------------------------------------------------------

    ProfessionalPatientAccess.objects.create(
        patient=patient,
        professional=request.user,
        status="pending"
    )

    messages.success(
        request,
        (
            f"Access request sent to "
            f"{patient.patient_name}."
        )
    )

    return redirect(
        "health_wallet:professional_access_status"
    )



@login_required
def manage_professional_access(request):

    if getattr(request.user, "role", None) != "PATIENT":
        raise PermissionDenied(
            "Only patient users can manage professional access."
        )

    patients = Patient.objects.filter(
        user=request.user
    )

    access_requests = ProfessionalPatientAccess.objects.filter(
        patient__in=patients
    ).select_related(
        "patient",
        "professional"
    ).order_by(
        "-requested_at"
    )

    return render(
        request,
        "health_wallet/manage_professional_access.html",
        {
            "patients": patients,
            "access_requests": access_requests,
        }
    )


@login_required
def approve_professional_access(request, access_id):

    if getattr(request.user, "role", None) != "PATIENT":
        raise PermissionDenied(
            "Only the patient can approve professional access."
        )

    if request.method != "POST":
        raise PermissionDenied(
            "Access approval must use POST."
        )

    access = get_object_or_404(
        ProfessionalPatientAccess.objects.select_related(
            "patient",
            "professional"
        ),
        access_id=access_id
    )

    if access.patient.user_id != request.user.id:
        raise PermissionDenied(
            "You cannot approve access for another patient's profile."
        )

    access.status = "active"
    access.approved_at = timezone.now()
    access.revoked_at = None

    access.save(
        update_fields=[
            "status",
            "approved_at",
            "revoked_at",
        ]
    )

    messages.success(
        request,
        (
            f"Access granted to "
            f"{access.professional.get_full_name() or access.professional.username}."
        )
    )

    return redirect(
        "health_wallet:manage_professional_access"
    )





@login_required
def reject_professional_access(request, access_id):

    if getattr(request.user, "role", None) != "PATIENT":
        raise PermissionDenied(
            "Only the patient can reject professional access."
        )

    if request.method != "POST":
        raise PermissionDenied(
            "Access rejection must use POST."
        )

    access = get_object_or_404(
        ProfessionalPatientAccess,
        access_id=access_id
    )

    if access.patient.user_id != request.user.id:
        raise PermissionDenied(
            "You cannot reject access for another patient's profile."
        )

    access.status = "rejected"
    access.approved_at = None

    access.save(
        update_fields=[
            "status",
            "approved_at",
        ]
    )

    messages.success(
        request,
        "Professional access request rejected."
    )

    return redirect(
        "health_wallet:manage_professional_access"
    )





@login_required
def revoke_professional_access(request, access_id):

    if getattr(request.user, "role", None) != "PATIENT":
        raise PermissionDenied(
            "Only the patient can revoke professional access."
        )

    if request.method != "POST":
        raise PermissionDenied(
            "Access revocation must use POST."
        )

    access = get_object_or_404(
        ProfessionalPatientAccess,
        access_id=access_id
    )

    if access.patient.user_id != request.user.id:
        raise PermissionDenied(
            "You cannot revoke another patient's professional access."
        )

    access.status = "revoked"
    access.revoked_at = timezone.now()

    access.save(
        update_fields=[
            "status",
            "revoked_at",
        ]
    )

    messages.success(
        request,
        "Professional access has been revoked."
    )

    return redirect(
        "health_wallet:manage_professional_access"
    )



@login_required
def professional_request_access(request):
    """
    Professional searches for a patient and requests
    access to that patient's Health Wallet.
    """

    if getattr(request.user, "role", None) != "PROFESSIONAL":
        raise PermissionDenied(
            "Only healthcare professionals can request patient access."
        )

    search_query = request.GET.get(
        "q",
        ""
    ).strip()

    patients = Patient.objects.none()

    if search_query:

        patients = Patient.objects.filter(
            patient_code__iexact=search_query
        )

        if not patients.exists():

            patients = Patient.objects.filter(
                patient_name__icontains=search_query
            ).order_by(
                "patient_name"
            )[:20]

    # ---------------------------------------------------------
    # EXISTING ACCESS INFORMATION
    # ---------------------------------------------------------

    access_map = {}

    if patients.exists():

        access_records = ProfessionalPatientAccess.objects.filter(
            professional=request.user,
            patient__in=patients
        )

        access_map = {
            access.patient_id: access
            for access in access_records
        }

    return render(
        request,
        "health_wallet/professional_request_access.html",
        {
            "search_query": search_query,
            "patients": patients,
            "access_map": access_map,
        }
    )


@login_required
def professional_access_status(request):

    if getattr(request.user, "role", None) != "PROFESSIONAL":
        raise PermissionDenied(
            "Only healthcare professionals can view access requests."
        )

    access_requests = ProfessionalPatientAccess.objects.filter(
        professional=request.user
    ).select_related(
        "patient"
    ).order_by(
        "-requested_at"
    )

    return render(
        request,
        "health_wallet/professional_access_status.html",
        {
            "access_requests": access_requests,
        }
    )



@login_required
def professional_patient_records(
    request,
    patient_id
):

    if getattr(request.user, "role", None) != "PROFESSIONAL":
        raise PermissionDenied(
            "Only healthcare professionals can access this page."
        )

    patient = get_object_or_404(
        Patient,
        patient_id=patient_id
    )

    # ---------------------------------------------------------
    # SECURITY
    # ---------------------------------------------------------

    if not professional_has_access(
        request.user,
        patient
    ):
        raise PermissionDenied(
            "You do not have active access to this patient's records."
        )

    # ---------------------------------------------------------
    # REDIRECT TO SAME RECORD PAGE
    # ---------------------------------------------------------

    return redirect(
        "health_wallet:all_records",
        patient_id=patient.patient_id
    )



