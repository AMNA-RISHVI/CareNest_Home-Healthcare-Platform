from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "about-us/",
        views.about_us,
        name="about_us"
    ),

    path(
        "services/",
        views.services,
        name="services"
    ),

    path(
        "process/",
        views.process,
        name="process"
    ),

    path(
        "families/",
        views.families,
        name="families"
    ),

    path(
        "expats/",
        views.expats,
        name="expats"
    ),

    path(
        "faq/",
        views.faq,
        name="faq"
    ),

    path(
        "contact/",
        views.contact,
        name="contact"
    ),

]