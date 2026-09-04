from django import forms
from .models import Professionals


class ProfessionalRegistrationForm(forms.ModelForm):
    district = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    description = forms.CharField(max_length=100)

    class Meta:
        model = Professionals
        fields = [
            "service_type",
            "qualifications",
            "qualifications_file",
            "experience",
            "consultation_fee",
            "language",
            "bio",
            "nic_number",
            
        ]

        widgets = {
            "service_type": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "qualifications": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter your qualifications"
                }
            ),

            "experience": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Describe your experience"
                }
            ),

            "consultation_fee": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter consultation fee",
                    "step": "0.01"
                }
            ),

            "language": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Sinhala, English, Tamil"
                }
            ),

            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Tell us about yourself"
                }
            ),

            "nic_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter NIC number"
                }
            ),

           
        }