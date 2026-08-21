from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # <-- ADD THIS IMPORT

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('adminpanel/', include('adminpanel.urls')),
    path('professionalpanel/', include('professionalpanel.urls')),
]