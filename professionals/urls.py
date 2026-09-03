from django.urls import path
from .import views

urlpatterns=[
        path('register/',
              views.professionals,
                name='professionals'),  

        path(
            'profile/', 
            views.professional_profile,
            name='professional_profile'),

        

        path('search/',
            views.find_professional, 
            name='find_professional'),

        
]