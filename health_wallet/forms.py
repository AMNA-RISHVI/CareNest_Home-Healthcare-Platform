from django import forms

from .models import (
    Allergy,
    ChronicCondition,
    Prescription,
    LabReport,
    VaccinationRecord,
    MedicalHistory,
)


class AllergyForm(forms.ModelForm):

    class Meta:
        model = Allergy

        fields = [
            "allergy_name",
            "severity",
            "reaction",
            "notes",
        ]

        widgets = {

            "allergy_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Penicillin"
                }
            ),

            "severity": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "reaction": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Skin rash, breathing difficulty"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Additional notes"
                }
            ),
        }





class ChronicConditionForm(forms.ModelForm):

    class Meta:
        model = ChronicCondition

        fields = [
            "condition_name",
            "diagnosed_date",
            "status",
            "notes",
        ]

        widgets = {

            "condition_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Diabetes"
                }
            ),

            "diagnosed_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Additional information"
                }
            ),
        }



class PrescriptionForm(forms.ModelForm):

    class Meta:
        model = Prescription

        fields = [
            "title",
            "medication",
            "dosage",
            "instructions",
            "prescription_date",
            "prescription_file",
            "notes",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Prescription - Hypertension"
                }
            ),

            "medication": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Amlodipine"
                }
            ),

            "dosage": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "e.g. 5mg once daily"
                }
            ),

            "instructions": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Instructions from healthcare professional"
                }
            ),

            "prescription_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "prescription_file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".jpg,.jpeg,.png,.pdf"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Additional notes"
                }
            ),
        }




class LabReportForm(forms.ModelForm):

    class Meta:
        model = LabReport

        fields = [
            "report_name",
            "test_date",
            "laboratory_name",
            "result_summary",
            "report_file",
            "notes",
        ]

        widgets = {

            "report_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Full Blood Count"
                }
            ),

            "test_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "laboratory_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Laboratory / Hospital name"
                }
            ),

            "result_summary": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter important results"
                }
            ),

            "report_file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".jpg,.jpeg,.png,.pdf"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Additional notes"
                }
            ),
        }



class VaccinationRecordForm(forms.ModelForm):

    class Meta:
        model = VaccinationRecord

        fields = [
            "vaccine_name",
            "vaccination_date",
            "dose",
            "next_due_date",
            "provider",
            "notes",
        ]

        widgets = {

            "vaccine_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. COVID-19"
                }
            ),

            "vaccination_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "dose": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Dose 2"
                }
            ),

            "next_due_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "provider": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Hospital / vaccination provider"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Additional notes"
                }
            ),
        }



class MedicalHistoryForm(forms.ModelForm):

    class Meta:
        model = MedicalHistory

        fields = [
            "title",
            "description",
            "event_date",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Appendectomy"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe the medical event"
                }
            ),

            "event_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
        }



        