from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

# Create your views here.
def presupuesto(request):
    return render(request,'Asesor/presupuesto.html')