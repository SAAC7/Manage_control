from django.urls import path, include
from Asesores import views

urlpatterns = [
    path('ase', views.presupuesto_list)
]