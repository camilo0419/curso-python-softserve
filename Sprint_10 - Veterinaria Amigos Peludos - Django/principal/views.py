from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from conexion import crear_conexion  
from datetime import date
from .models import Cliente, Mascota
from .forms import ClienteForm, MascotaForm

def inicio(request):
    fecha = request.GET.get('fecha', date.today().isoformat())
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT consultas.id, consultas.motivo, consultas.diagnostico, mascotas.nombre_mascota
        FROM consultas
        JOIN mascotas ON consultas.mascota_id = mascotas.id
        WHERE consultas.fecha = ?
    """, (fecha,))
    consultas = cursor.fetchall()
    conexion.close()

    return render(request, 'principal/inicio.html', {
        'consultas': consultas,
        'fecha': fecha
    })

def clientes(request):
    return render(request, 'principal/clientes.html')

def mascotas(request):
    return render(request, 'principal/mascotas.html')

#ORM Clientes

def lista_clientes(request):
    clientes = Cliente.objects.filter(activo=True)
    return render(request, 'principal/lista_clientes.html', {'clientes': clientes})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'principal/formulario_cliente.html', {'form': form})

def editar_cliente(request, cedula):
    cliente = get_object_or_404(Cliente, cedula=cedula)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'principal/formulario_cliente.html', {'form': form})

def eliminar_cliente(request, cedula):
    cliente = get_object_or_404(Cliente, cedula=cedula)
    cliente.activo = False
    cliente.save()
    return redirect('lista_clientes')

#ORM Mascotas

def lista_mascotas(request):
    mascotas = Mascota.objects.all()
    return render(request, 'principal/lista_mascotas.html', {'mascotas': mascotas})

def crear_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_mascotas')
    else:
        form = MascotaForm()
    return render(request, 'principal/formulario_mascota.html', {'form': form, 'modo': 'Crear'})


def editar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('lista_mascotas')
    else:
        form = MascotaForm(instance=mascota)
    return render(request, 'principal/formulario_mascota.html', {'form': form, 'modo': 'Editar'})


def eliminar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    mascota.delete()
    return redirect('lista_mascotas')
