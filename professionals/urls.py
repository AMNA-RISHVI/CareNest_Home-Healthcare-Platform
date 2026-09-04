from django.urls import path
from .import views

urlpatterns=[
        path('register/',
              views.professional_register,
                name='professional_register'),  

        path(
            'profile/', 
            views.professional_profile,
            name='professional_profile'),

        

        path('search/',
            views.find_professional, 
            name='find_professional'),


        path('board/',
                    views.professional_dashboard, 
                    name='professional_dashboard'),
        
]