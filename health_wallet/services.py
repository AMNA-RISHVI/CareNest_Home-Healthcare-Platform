from django.core.exceptions import PermissionDenied

from patient_dashboard.models import Patient

from .models import (
    ProfessionalPatientAccess,
    HealthRecordChange,
)


def get_patient_for_user(user, patient_id):
    """
    Return a patient profile belonging to the logged-in user.

    Patients can only access their own family profiles.
    """

    return Patient.objects.filter(
        patient_id=patient_id,
        user=user
    ).first()



def is_patient_owner(user, patient):
    """
    Check whether the logged-in user is the patient account
    that owns this family profile.
    """

    return (
        user.is_authenticated
        and getattr(user, "role", None) == "PATIENT"
        and patient.user_id == user.id
    )


def is_patient_user(user):
    """
    Check whether the account is a patient account.
    """

    return (
        user.is_authenticated
        and getattr(user, "role", None) == "PATIENT"
    )


def professional_has_access(user, patient):
    """
    A professional can access a patient's health wallet only
    when the patient has an ACTIVE access relationship.
    """

    if not user.is_authenticated:
        return False

    if getattr(user, "role", None) != "PROFESSIONAL":
        return False

    return ProfessionalPatientAccess.objects.filter(
        patient=patient,
        professional=user,
        status="active"
    ).exists()



def can_access_patient_records(user, patient):
    """
    Determines whether the logged-in user can view
    the patient's health records.
    """

    # Patient owner
    if is_patient_owner(user, patient):
        return True

    # Connected healthcare professional
    if professional_has_access(user, patient):
        return True

    return False


def can_modify_patient_records(user, patient):
    """
    Determines whether the logged-in user can add/edit/delete
    health records.

    Patient owner has highest authority.
    Connected professionals may modify records only when
    active access has been granted.
    """

    # ---------------------------------------------------------
    # PATIENT OWNER
    # ---------------------------------------------------------

    if is_patient_owner(user, patient):
        return True

    # ---------------------------------------------------------
    # CONNECTED PROFESSIONAL
    # ---------------------------------------------------------

    if professional_has_access(user, patient):
        return True

    return False


def require_record_access(user, patient):
    """
    Raise PermissionDenied if the user cannot access records.
    """

    if not can_access_patient_records(user, patient):
        raise PermissionDenied(
            "You do not have permission to access this patient's health records."
        )


def require_record_modify_access(user, patient):
    """
    Raise PermissionDenied if the user cannot modify records.
    """

    if not can_modify_patient_records(user, patient):
        raise PermissionDenied(
            "You do not have permission to modify this patient's health records."
        )



def can_view_health_record_changes(user, patient):
    """
    Determine whether the logged-in user can view
    audit history for a patient's health records.

    Patient owner:
        Full access.

    Connected professional:
        Access only while active access exists.
    """

    # Patient owner has highest authority
    if is_patient_owner(user, patient):
        return True

    # Professional must have active access
    if professional_has_access(user, patient):
        return True

    return False




def create_health_record_change(
    patient,
    actor,
    category,
    record_id,
    action,
    description
):
    """
    Create an audit entry whenever a health record
    is created, updated or deleted.
    """

    HealthRecordChange.objects.create(

        patient=patient,

        actor=actor,

        actor_role=getattr(
            actor,
            "role",
            "UNKNOWN"
        ),

        category=category,

        record_id=record_id,

        action=action,

        description=description,
    )




