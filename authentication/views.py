from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (
    UserRegistrationForm,
    LoginForm,
    ForgotPasswordForm,
    ResetPasswordForm,
    ProfileUpdateForm,
    ChangePasswordForm,
)
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

from .token import account_activation_token
from .token import password_reset_token

from .utils import send_verification_email
from .utils import send_password_reset_email

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from django.contrib.auth import get_user_model

from django.contrib.auth import update_session_auth_hash

from .decorators import role_required

def register(request):

    if request.user.is_authenticated:
        return redirect_user_dashboard(
            request.user
        )

    if request.method == "POST":

        form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():

            user = form.save(commit=False)

            user.email_verified = False

            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))

            token = account_activation_token.make_token(user)

            verification_url = (
                f"http://{get_current_site(request).domain}"
                + reverse(
                    "activate",
                    kwargs={
                        "uidb64": uid,
                        "token": token,
                    }
                )
            )

            send_verification_email(
                request,
                user,
                verification_url,
            )

            return redirect("verify_email_done")

        else:

            messages.error(
                request,
                "Please correct the errors below and try again."
            )


    else:

        form = UserRegistrationForm()

    return render(
        request,
        "authentication/register.html",
        {
            "form": form
        }
    )



def user_login(request):

    # If already logged in, redirect to the correct dashboard
    if request.user.is_authenticated:

        return redirect_user_dashboard(request.user)

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data.get("username")

            password = form.cleaned_data.get("password")

            remember = form.cleaned_data.get("remember_me")

            user = authenticate(
                username=username,
                password=password
            )

            # Invalid username/password
            if user is None:

                messages.error(
                    request,
                    "Invalid Username or Password."
                )

                return redirect("login")

            # Email not verified
            if not user.email_verified:
                messages.error(
                    request,
                    "Please verify your email before logging in."
                )

                return redirect("login")

            # Inactive account
            if not user.is_active:

                messages.error(
                    request,
                    "Your account has been disabled. Please contact the administrator."
                )

                return redirect("login")

            # Login user
            login(request, user)

            # Remember Me
            if remember:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # Expires when browser closes


            messages.success(
                request,
                f"Welcome {user.full_name}"
            )

            return redirect_user_dashboard(user)

        else:

            messages.error(
                request,
                "Invalid Username or Password."
            )
    else:
        form=LoginForm()

    return render(
        request,
        "authentication/login.html",
        {
            "form": form
        }
    )

@login_required
def user_logout(request):

    logout(request)

    messages.success(
        request,
        "You have logged out successfully."
    )

    return redirect("login")


def redirect_user_dashboard(user):

    if user.role == "ADMIN":
        return redirect("/admin-dashboard/")

    elif user.role == "PROFESSIONAL":
        return redirect("/professional-dashboard/")

    else:
        return redirect("/patient-dashboard/")

    


@login_required
@role_required("PATIENT")
def patient_dashboard(request):

    return render(
        request,
        "patient_dashboard.html"
    )


@login_required
@role_required("PROFESSIONAL")
def professional_dashboard(request):

    return render(
        request,
        "professional_dashboard.html"
    )


@login_required
@role_required("ADMIN")
def admin_dashboard(request):

    return render(
        request,
        "admin_dashboard.html"
    )



User = get_user_model()


def activate(request, uidb64, token):

    try:

        uid = force_str(
            urlsafe_base64_decode(uidb64)
        )

        user = User.objects.get(pk=uid)

    except Exception:

        user = None

    if user and account_activation_token.check_token(user, token):

        user.email_verified = True

        user.save()

        messages.success(
            request,
            "Email verified successfully. You can now log in."
        )

        return redirect("login")

    messages.error(
        request,
        "Invalid or expired verification link."
    )

    return redirect("register")



@login_required
def profile(request):

    return render(

        request,

        "authentication/profile.html",

        {
            "user":request.user
        }

    )


def forgot_password(request):

    if request.user.is_authenticated:
        return redirect_user_dashboard(
            request.user
        )

    if request.method == "POST":

        form = ForgotPasswordForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            try:

                user = User.objects.get(email=email)

                uid = urlsafe_base64_encode(
                    force_bytes(user.pk)
                )

                token = password_reset_token.make_token(user)

                reset_url = (
                    f"http://{get_current_site(request).domain}"
                    + reverse(
                        "reset_password",
                        kwargs={
                            "uidb64": uid,
                            "token": token,
                        }
                    )
                )

                send_password_reset_email(
                    request,
                    user,
                    reset_url,
                )

                return redirect("password_reset_done")

            except User.DoesNotExist:

                messages.error(
                    request,
                    "No account found with this email."
                )

    else:

        form = ForgotPasswordForm()

    return render(
        request,
        "authentication/forgot_password.html",
        {
            "form": form
        }
    )


def reset_password(request, uidb64, token):

    try:

        uid = force_str(
            urlsafe_base64_decode(uidb64)
        )

        user = User.objects.get(pk=uid)

    except Exception:

        user = None

    if user is None:

        messages.error(
            request,
            "Invalid password reset link."
        )

        return redirect("forgot_password")

    if not password_reset_token.check_token(user, token):

        messages.error(
            request,
            "Password reset link has expired or is invalid."
        )

        return redirect("forgot_password")

    if request.method == "POST":

        form = ResetPasswordForm(
            user,
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Password has been reset successfully. Please login."
            )

            return redirect("login")

    else:

        form = ResetPasswordForm(user)

    return render(
        request,
        "authentication/reset_password.html",
        {
            "form": form
        }
    )

def password_reset_done(request):

    return render(
        request,
        "authentication/password_reset_done.html"
    )

def verify_email_done(request):

    return render(
        request,
        "authentication/verify_email_done.html"
    )


@login_required
def edit_profile(request):

    if request.method == "POST":

        form = ProfileUpdateForm(

            request.POST,

            request.FILES,

            instance=request.user

        )

        if form.is_valid():

            form.save()

            messages.success(

                request,

                "Profile updated successfully."

            )

            return redirect("profile")

        else:

            messages.error(

                request,

                "Please correct the highlighted fields."

            )

    else:

        form = ProfileUpdateForm(

            instance=request.user

        )

    return render(

        request,

        "authentication/edit_profile.html",

        {
            "form":form
        }

    )


@login_required
def change_password(request):

    if request.method == "POST":

        form = ChangePasswordForm(

            request.user,

            request.POST

        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request, 
                user
            )

            messages.success(
                request,
                "Password changed successfully."
            )

            return redirect("profile")

        else:
            messages.error(
                request,
                "Please correct the errors below."
            )

    else:
        form = ChangePasswordForm(
            request.user
        )

    return render(
        request,
        "authentication/change_password.html",
        {
            "form":form
        }
    )