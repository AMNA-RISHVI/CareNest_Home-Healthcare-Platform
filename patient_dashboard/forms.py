from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Patient


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient

        fields = [
            'patient_name',
            'relationship',
            'profile_picture',
            'dob',
            'gender',
            'blood_group',
            'emergency_contact',
        ]

        widgets = {
            'patient_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name',
            }),

            'relationship': forms.Select(attrs={
                'class': 'form-control',
            }),

            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),

            'dob': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),

            'gender': forms.Select(attrs={
                'class': 'form-control',
            }),

            'blood_group': forms.Select(attrs={
                'class': 'form-control',
            }),

            'emergency_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter emergency contact number',
            }),
        }

        labels = {
            'patient_name': 'Full Name',
            'relationship': 'Relationship',
            'dob': 'Date of Birth',
            'gender': 'Gender',
            'blood_group': 'Blood Group',
            'emergency_contact': 'Emergency Contact',
        }

    def clean_patient_name(self):
        name = self.cleaned_data['patient_name'].strip()

        if len(name) < 2:
            raise ValidationError(
                'Please enter a valid name.'
            )

        return name


    def clean_profile_picture(self):
        image = self.cleaned_data.get('profile_picture')

        if image:
            max_size = 5 * 1024 * 1024  # 5 MB

            if image.size > max_size:
                raise forms.ValidationError(
                    'Profile picture must be smaller than 5 MB.'
                )

        return image


    def clean_dob(self):
        dob = self.cleaned_data.get('dob')

        if dob and dob > timezone.localdate():
            raise ValidationError(
                'Date of birth cannot be in the future.'
            )

        return dob