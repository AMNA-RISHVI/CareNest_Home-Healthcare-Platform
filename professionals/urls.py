from django.urls import path
from .import views

urlpatterns=[
        path('register/', views.professionals, name='professionals'),         
        path(
            'profile/', 
            views.professional_profile, name='professional_profile'),
        path('available/',views.availability, name='availability'),
        path('search/', views.find_professional, name='find_professional'),
        path('prodash/',views.professional_dashboard, name='prof_dash'),
]