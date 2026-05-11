from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('why-work-with-us/', views.why_us, name='why_us'),
    path('contact/', views.contact, name='contact'),
]
