from django import forms
from .models import Professionals


class ProfessionalRegistrationForm(forms.ModelForm):

    class Meta:
        model = Professionals

        fields = [
            'service_type',
            'qualifications',
            'qualifications_file',
            'experience',
            'consultation_fee',
            'language',
            'bio',
            'nic_number',
            'professional_code',
        ]