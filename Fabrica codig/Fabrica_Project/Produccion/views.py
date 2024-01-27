from django.shortcuts import render

# Create your views here.
def trabajo(request):
    return render(request,'Produccion/trabajos.html')