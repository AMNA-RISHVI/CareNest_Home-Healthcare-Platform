from django.shortcuts import render
from django.db.models import Avg

from authentication.models import User

def home(request):

    return render(
        request,
        "landing/home.html",
    )


def about_us(request):

    return render(
        request,
        "landing/partials/about.html"
    )

def services(request):

    return render(
        request,
        "landing/partials/services.html"
    )

def process(request):
    return render(
        request,
        "landing/process.html"
    )

def families(request):
    return render(
        request,
        "landing/families.html"
    )

def expats(request):
    return render(
        request,
        "landing/expats.html"
    )

def faq(request):
    return render(
        request, 
        "landing/faq.html"
    )

def contact(request):
    return render(
        request,
        "landing/contact.html"
    )

