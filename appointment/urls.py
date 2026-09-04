from django.urls import path
from .import views

urlpatterns=[
        path('',
             views.appointment,
             name='appointment'),

        path('review/',
             views.review_rate,
             name='review_rate'),

        path('status/',
             views.appointment_status,
             name='appointment_status'),

        path('book/<int:professional_id>/',
             views.book_appointment,
             name='book_appointment'),

        path('history/',
             views.appointment_history,
             name='appointment_history'),
]