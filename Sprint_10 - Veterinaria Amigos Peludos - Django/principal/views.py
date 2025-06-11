from django.shortcuts import render

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def servicios(request):
    return render(request, 'servicios.html')

def placeholder(request):
    return render(request, 'placeholder.html')