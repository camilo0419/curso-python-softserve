from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from django.db import models
from conexion import crear_conexion  
from datetime import date
from .models import Cliente, Mascota, Consulta, FormulaMedica, Medicamento
from .forms import ClienteForm, MascotaForm, ConsultaForm, FormulaMedicaForm
from django.forms import modelformset_factory
from django.templatetags.static import static
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

def inicio(request):
    fecha_str = request.GET.get('fecha')
    if fecha_str:
        fecha = date.fromisoformat(fecha_str)
    else:
        fecha = date.today()

    consultas = Consulta.objects.filter(fecha=fecha).select_related('mascota')

    context = {
        'fecha': fecha.strftime('%Y-%m-%d'),  # Formato compatible con el input date
        'consultas': consultas,
    }
    return render(request, 'principal/inicio.html', context)

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
    mascotas = Mascota.objects.filter(activo=True)
    return render(request, 'principal/lista_mascotas.html', {'mascotas': mascotas})

def crear_mascota(request):
    cliente_id = request.GET.get('cliente_id')
    cliente = Cliente.objects.filter(id=cliente_id).first() if cliente_id else None

    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)
            if cliente:
                mascota.cliente = cliente  # aseguramos que no cambien el cliente
            mascota.save()
            return redirect('lista_mascotas')
    else:
        initial_data = {'cliente': cliente.id} if cliente else {}
        form = MascotaForm(initial=initial_data)

    return render(request, 'principal/formulario_mascota.html', {
        'form': form,
        'modo': 'Crear',
        'cliente_bloqueado': cliente is not None,
        'cliente': cliente  # lo usamos para mostrar el nombre
    })




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
    mascota.activo = False
    mascota.save()
    return redirect('lista_mascotas')

def buscar_clientes(request):
    q = request.GET.get('q', '').strip().lower()
    coincidencias = Cliente.objects.filter(
        activo=True
    ).filter(
        models.Q(nombre__icontains=q) | models.Q(cedula__icontains=q)
    ).values('id', 'nombre', 'cedula')[:10]

    return JsonResponse(list(coincidencias), safe=False)

def mascotas_por_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    mascotas = Mascota.objects.filter(cliente=cliente)
    return render(request, 'principal/mascotas_por_cliente.html', {'cliente': cliente, 'mascotas': mascotas})



#ORM Consultas
def lista_consultas(request):
    consultas = Consulta.objects.select_related('mascota').order_by('-fecha')
    return render(request, 'principal/lista_consultas.html', {'consultas': consultas})

def crear_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_consultas')
    else:
        form = ConsultaForm()
    return render(request, 'principal/formulario_consulta.html', {'form': form})

def editar_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('lista_consultas')
    else:
        form = ConsultaForm(instance=consulta)
    return render(request, 'principal/formulario_consulta.html', {'form': form})

def eliminar_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    consulta.delete()
    return redirect('lista_consultas')

def detalle_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    hay_formula = FormulaMedica.objects.filter(consulta=consulta).exists()

    return render(request, 'principal/detalle_consulta.html', {
        'consulta': consulta,
        'hay_formula': hay_formula
    })



#Historia Clinica

from .models import Mascota, Consulta
from django.shortcuts import render, get_object_or_404

def historia_clinica(request, mascota_id):
    mascota = get_object_or_404(Mascota, pk=mascota_id)
    consultas = mascota.consultas.all().order_by('-fecha')  # related_name='consultas'
    return render(request, 'principal/historia_clinica.html', {
        'mascota': mascota,
        'consultas': consultas
    })


def exportar_historia_pdf(request, mascota_id):
    mascota = get_object_or_404(Mascota, pk=mascota_id)
    consultas = mascota.consultas.all().order_by('-fecha')

    # Ruta absoluta del logo
    logo_url = request.build_absolute_uri(static('principal/img/logo.png'))

    html_string = render_to_string('principal/historia_clinica_pdf.html', {
        'mascota': mascota,
        'consultas': consultas,
        'logo_url': logo_url
    })

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="historia_clinica_{mascota.nombre_mascota}.pdf"'
    return response

def buscar_mascotas(request):
    q = request.GET.get('q', '')
    resultados = Mascota.objects.filter(
        Q(nombre_mascota__icontains=q) | Q(cliente__nombre__icontains=q)
    )[:10]

    data = [
        {
            'id': m.id,
            'nombre_mascota': m.nombre_mascota,
            'cliente': m.cliente.nombre
        } for m in resultados
    ]
    return JsonResponse(data, safe=False)

#Formula medica

def crear_formula_medica(request, consulta_id):
    consulta = get_object_or_404(Consulta, pk=consulta_id)

    if not consulta.req_medicamentos:
        return redirect('detalle_consulta', consulta_id=consulta.id)

    if request.method == 'POST':
        form = FormulaMedicaForm(request.POST)
        if form.is_valid():
            formula = form.save(commit=False)
            formula.consulta = consulta
            formula.save()
            return redirect('detalle_consulta', consulta_id=consulta.id)
    else:
        form = FormulaMedicaForm()

    return render(request, 'principal/formula_medica_form.html', {
        'form': form,
        'consulta': consulta
    })

def asignar_medicamentos(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)

    if consulta.med_entregado:
        messages.warning(request, "🚫 Ya se entregaron medicamentos para esta consulta.")
        return redirect('detalle_consulta', consulta_id=consulta.id)

    medicamentos = Medicamento.objects.filter(activo=True).order_by('nombre_med')

    if request.method == 'POST':
        accion = request.POST.get('accion')
        formulas = []

        index = 0
        while True:
            med_id = request.POST.get(f'medicamento_{index}')
            if not med_id:
                break

            dosis = request.POST.get(f'dosis_{index}', '')
            frecuencia = request.POST.get(f'frecuencia_{index}', '')
            duracion = request.POST.get(f'duracion_{index}', '')
            via = request.POST.get(f'via_administracion_{index}', '')
            observaciones = request.POST.get(f'observaciones_{index}', '')

            medicamento = Medicamento.objects.filter(id=med_id).first()
            if medicamento:
                FormulaMedica.objects.create(
                    consulta=consulta,
                    medicamento=medicamento,
                    dosis=dosis,
                    frecuencia=frecuencia,
                    duracion=duracion,
                    via_administracion=via,
                    observaciones=observaciones
                )
                formulas.append(medicamento.nombre_med)

            index += 1

        if accion == 'guardar':
            messages.success(request, f"💾 Fórmula guardada con {len(formulas)} medicamentos.")
            return redirect('detalle_consulta', consulta_id=consulta.id)


        elif accion == 'entregar':
            consulta.med_entregado = True
            consulta.save()
            messages.success(request, f"🚚 Medicamentos entregados: {', '.join(formulas)}")
            return redirect('detalle_consulta', consulta_id=consulta.id)

    # Si es GET
    return render(request, 'principal/formulario_formula_medica.html', {
        'consulta': consulta,
        'medicamentos': medicamentos,
        'guardado': False
    })

@csrf_protect
def ver_formula_medica(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    formulas = FormulaMedica.objects.filter(consulta=consulta)

    if request.method == 'POST' and request.POST.get('accion') == 'entregar':
        if not consulta.med_entregado:
            consulta.med_entregado = True
            consulta.save()
            messages.success(request, "🚚 Medicamentos marcados como entregados.")
            return redirect('ver_formula', consulta_id=consulta.id)

    return render(request, 'principal/ver_formula_medica.html', {
        'consulta': consulta,
        'formulas': formulas
    })


def asignar_cirugia(request, consulta_id):
    # Por ahora puede estar vacía o con un return básico
    return render(request, 'principal/asignar_cirugia.html', {'consulta_id': consulta_id})

def lista_formulas(request):
    query = request.GET.get('buscar', '')
    formulas = Consulta.objects.filter(req_medicamentos=True)

    if query:
        formulas = formulas.filter(
            mascota__nombre_mascota__icontains=query
        ) | formulas.filter(
            mascota__cliente__nombre__icontains=query
        )

    context = {
        'formulas': formulas,
        'query': query,
    }
    return render(request, 'principal/lista_formulas.html', context)
