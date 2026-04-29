from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    # Include Django's built-in auth URLs (login, logout)
    path('', include('django.contrib.auth.urls')),
    # Registration page
    path('register/', views.register, name='register'),
]