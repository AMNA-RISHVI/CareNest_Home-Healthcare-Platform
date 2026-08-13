from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm

class UserRegistrationForm(UserCreationForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'auth-input',
                'placeholder': 'Create a password',
                "id": "id_password1",
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'auth-input',
                'placeholder': 'Confirm your password'
            }
        )
    )

    class Meta:
        model = User
        fields = [
            'username',
            'full_name',
            'email',
            'phone',
            'address',
            'district',
            'gender',
            'dob',
            'profile_picture',
            'role',
            'password1',
            'password2',
        ]

    widgets = {

        'full_name': forms.TextInput(
            attrs={
                'class': 'auth-input',
                'placeholder': 'Enter your full name'
            }
        ),

        'username': forms.TextInput(
            attrs={
                'class': 'auth-input',
                'placeholder': 'Choose a username'
            }
        ),

        'email': forms.EmailInput(
            attrs={
                'class': 'auth-input',
                'placeholder': 'Enter your email'
            }
        ),

        'phone': forms.TextInput(
            attrs={
                'class': 'auth-input',
                'placeholder': 'Enter your phone number',
                "maxlength": "12",
                "inputmode": "tel",
                "autocomplete": "tel",
            }
        ),

        'address': forms.Textarea(
            attrs={
                'class': 'auth-input',
                'placeholder': 'Enter your address',
                'rows': 3
            }
        ),

        'district': forms.Select(
            attrs={
                'class': 'auth-select'
            }
        ),

        'gender': forms.Select(
            attrs={
                'class': 'auth-select'
            }
        ),

        'dob': forms.DateInput(
            attrs={
                'class': 'auth-input',
                'type': 'date'
            }
        ),

        'profile_picture': forms.ClearableFileInput(
            attrs={
                'class': 'auth-input'
            }
        ),

        'role': forms.Select(
            attrs={
                'class': 'auth-select'
            }
        ),
    }


    def clean_phone(self):

        phone = self.cleaned_data.get("phone")

        if not phone:
            raise forms.ValidationError(
                "Phone number is required."
            )

        phone = phone.strip().replace(" ", "")

        # Local Sri Lankan format
        if re.fullmatch(r"07\d{8}", phone):
            phone = "+94" + phone[1:]

        # International Sri Lankan format
        elif re.fullmatch(r"\+947\d{8}", phone):

            pass

        else:
            raise forms.ValidationError(
                "Enter a valid Sri Lankan mobile number. "
                "Use 0712345678 or +94712345678."
            )

        return phone

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            css_class = field.widget.attrs.get("class", "")

            if self.errors.get(field_name):
                field.widget.attrs["class"] = css_class + " is-invalid"

            else:
                field.widget.attrs["class"] = css_class



class LoginForm(AuthenticationForm):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "auth-input",
                "placeholder": "Username"
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "auth-input",
                "placeholder": "Password"
            }
        )
    )

    remember_me = forms.BooleanField(
        required=False,
        initial=False
    )



class ForgotPasswordForm(PasswordResetForm):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your registered email"
            }
        )
    )


class ResetPasswordForm(SetPasswordForm):

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "New Password"
            }
        )
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password"
            }
        )
    )


class ProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            "full_name",
            "phone",
            "address",
            "district",
            "gender",
            "dob",
            "profile_picture",
        ]

        widgets = {

            "full_name": forms.TextInput(
                attrs={
                    "class": "auth-input",
                    "placeholder": "Enter your full name"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class":"auth-input",
                    "placeholder": "Enter your phone number",
                    "maxlength": "12",
                    "inputmode": "tel",
                    "autocomplete": "tel",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class":"auth-input",
                    "rows": 3,
                    "placeholder": "Enter your address"
                }
            ),

            "district": forms.Select(
                attrs={
                    "class":"auth-select"
                }
            ),

            "gender": forms.Select(
                attrs={
                    "class":"auth-select"
                }
            ),

            "dob": forms.DateInput(
                attrs={
                    "class":"auth-input",
                    "type":"date"
                }
            ),

            "profile_picture": forms.ClearableFileInput(
                attrs={
                    "class": "profile-file-input",
                    "accept": "image/png,image/jpeg"
                }
            ),

        }  

    def clean_phone(self):
    
        phone = self.cleaned_data.get("phone")
    
        if not phone:
            raise forms.ValidationError(
                "Phone number is required."
            )
    
        phone = phone.strip().replace(" ", "")
    
        # Local Sri Lankan format
        if re.fullmatch(r"07\d{8}", phone):
            phone = "+94" + phone[1:]
    
        # International Sri Lankan format
        elif re.fullmatch(r"\+947\d{8}", phone):
    
            pass
    
        else:
            raise forms.ValidationError(
                "Enter a valid Sri Lankan mobile number. "
                "Use 0712345678 or +94712345678."
            )
    
        return phone
        

    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)

        for field_name, field in self.fields.items():

            css = field.widget.attrs.get("class","")

            if self.errors.get(field_name):

                field.widget.attrs["class"] = css + " is-invalid"




class ChangePasswordForm(PasswordChangeForm):

    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "auth-input",
                "placeholder": "Enter your current password",
                "autocomplete": "current-password",
            }
        )
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "auth-input",
                "placeholder": "Create a new password",
                "autocomplete": "new-password",
                "id": "id_new_password1",
            }
        )
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "auth-input",
                "placeholder": "Confirm your new password",
                "autocomplete": "new-password",
                "id": "id_new_password2",
            }
        )
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():

            css = field.widget.attrs.get("class", "")

            if self.errors.get(field_name):

                field.widget.attrs["class"] = (
                    css + " is-invalid"
                )