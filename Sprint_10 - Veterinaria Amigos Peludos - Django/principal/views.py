from django.shortcuts import render

def inicio(request):
    return render(request, 'principal/inicio.html')

def clientes(request):
    return render(request, 'principal/clientes.html')

def mascotas(request):
    return render(request, 'principal/mascotas.html')
