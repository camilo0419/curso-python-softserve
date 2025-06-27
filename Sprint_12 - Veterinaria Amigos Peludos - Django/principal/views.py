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
from .models import Cliente, Mascota, Consulta, FormulaMedica, Medicamento, Profesional, Cirugia
from .forms import ClienteForm, MascotaForm, ConsultaForm, FormulaMedicaForm, MedicamentoForm, ProfesionalForm, CirugiaForm
from django.forms import modelformset_factory
from django.templatetags.static import static
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from principal.utils.export_excel import generar_excel
from django.core.paginator import Paginator


def inicio(request):
    cirugias = Cirugia.objects.filter(
        activo=True,
        fecha_prog__gte=date.today()
    ).order_by('fecha_prog', 'hora_prog')[:5]  # próximas 5

    return render(request, 'principal/inicio.html', {
        'cirugias': cirugias
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
    cliente = mascota.cliente  # Obtenemos el cliente actual (dueño)

    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            mascota_editada = form.save(commit=False)
            mascota_editada.cliente = cliente  # Evitamos que se cambie el dueño
            mascota_editada.save()
            return redirect('lista_mascotas')
    else:
        form = MascotaForm(instance=mascota)

    return render(request, 'principal/formulario_mascota.html', {
        'form': form,
        'modo': 'Editar',
        'cliente_bloqueado': True,
        'cliente': cliente
    })



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

def crear_consulta(request, mascota_id):
    mascota = get_object_or_404(Mascota, pk=mascota_id)
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.mascota = mascota
            consulta.save()
            return redirect('historia_clinica', mascota.id)
    else:
        form = ConsultaForm()
    return render(request, 'principal/formulario_consulta.html', {
        'form': form,
        'mascota': mascota
    })

def crear_consulta_general(request):
    # Redirige a una búsqueda de mascota o muestra error
    return HttpResponse("Selecciona una mascota para iniciar una consulta.")

def editar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            consulta = form.save()
            if consulta.req_cirugia and not Cirugia.objects.filter(consulta=consulta).exists():
                return redirect('asignar_cirugia', consulta_id=consulta.id)
            return redirect('detalle_consulta', consulta.id)
    else:
        form = ConsultaForm(instance=consulta)
    return render(request, 'principal/formulario_consulta.html', {'form': form})

def eliminar_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    consulta.delete()
    return redirect('lista_consultas')

def detalle_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    # Determinar el estado de medicamentos
    formulas = FormulaMedica.objects.filter(consulta=consulta)
    if not formulas.exists():
        estado_medicamentos = "pendiente_asignar"
    elif not consulta.med_entregado:
        estado_medicamentos = "pendiente_entregar"
    else:
        estado_medicamentos = "entregado"

    context = {
        'consulta': consulta,
        'estado_medicamentos': estado_medicamentos
    }
    return render(request, 'principal/detalle_consulta.html', context)



#Historia Clinica

from .models import Mascota, Consulta
from django.shortcuts import render, get_object_or_404
from datetime import datetime

def historia_clinica(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    consultas = mascota.consultas.select_related('mascota', 'mascota__cliente').prefetch_related('formulas__medicamento', 'cirugia').order_by('-fecha')
    hora_actual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    return render(request, 'principal/historia_clinica.html', {
        'mascota': mascota,
        'consultas': consultas,
        'hora_actual': hora_actual
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

def lista_medicamentos(request):
    medicamentos = Medicamento.objects.filter(activo=True).order_by('nombre_med')  # o el filtro que uses
    paginator = Paginator(medicamentos, 10)  # 10 por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'principal/lista_medicamentos.html', {
        'page_obj': page_obj
    })

def lista_profesionales(request):
    profesionales = Profesional.objects.filter(activo=True).order_by('nombre_prof')
    paginator = Paginator(profesionales, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'principal/lista_profesionales.html', {
        'page_obj': page_obj
    })

# Editar Medicamento
def editar_medicamento(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    if request.method == 'POST':
        form = MedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            return redirect('lista_medicamentos')
    else:
        form = MedicamentoForm(instance=medicamento)
    return render(request, 'principal/formulario_medicamento.html', {'form': form})

# Eliminar Medicamento
def eliminar_medicamento(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    if request.method == 'POST':
        medicamento.delete()
        return redirect('lista_medicamentos')
    return render(request, 'principal/confirmar_eliminar.html', {'objeto': medicamento, 'tipo': 'medicamento'})

# Editar Profesional
def editar_profesional(request, pk):
    profesional = get_object_or_404(Profesional, pk=pk)
    if request.method == 'POST':
        form = ProfesionalForm(request.POST, instance=profesional)
        if form.is_valid():
            form.save()
            return redirect('lista_profesionales')
    else:
        form = ProfesionalForm(instance=profesional)
    return render(request, 'principal/formulario_profesional.html', {'form': form})

# Eliminar Profesional
def eliminar_profesional(request, pk):
    profesional = get_object_or_404(Profesional, pk=pk)
    if request.method == 'POST':
        profesional.delete()
        return redirect('lista_profesionales')
    return render(request, 'principal/confirmar_eliminar.html', {'objeto': profesional, 'tipo': 'profesional'})

def crear_medicamento(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_medicamentos')
    else:
        form = MedicamentoForm()
    return render(request, 'principal/formulario_medicamento.html', {'form': form})


def crear_profesional(request):
    if request.method == 'POST':
        form = ProfesionalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_profesionales')
    else:
        form = ProfesionalForm()
    return render(request, 'principal/formulario_profesional.html', {'form': form})


def historial_cirugias(request, pk):
    return HttpResponse("🔧 Módulo de cirugías en construcción.")

def asignar_cirugia(request, consulta_id):
    consulta = get_object_or_404(Consulta, pk=consulta_id)

    if Cirugia.objects.filter(consulta=consulta).exists():
        return redirect('detalle_consulta', consulta_id=consulta.id)

    if request.method == 'POST':
        form = CirugiaForm(request.POST)
        if form.is_valid():
            cirugia = form.save(commit=False)
            cirugia.mascota = consulta.mascota
            cirugia.consulta = consulta
            cirugia.estado = "Programada" # 
            cirugia.save()
            messages.success(request, "✅ Cirugía programada correctamente.")
            return redirect('detalle_consulta', consulta.id)
    else:
        form = CirugiaForm()

    return render(request, 'principal/formulario_cirugia.html', {
        'form': form,
        'consulta': consulta
    })

def ver_cirugia(request, consulta_id):
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    cirugia = Cirugia.objects.filter(consulta=consulta).first()

    if not cirugia:
        messages.info(request, "ℹ️ No se encontró una cirugía registrada.")
        return redirect('asignar_cirugia', consulta_id=consulta.id)

    return render(request, 'principal/ver_cirugia.html', {
        'consulta': consulta,
        'cirugia': cirugia
    })

def editar_cirugia(request, consulta_id):
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    cirugia = consulta.cirugia.first() 

    if not cirugia:
        messages.warning(request, "No hay una cirugía programada para esta consulta.")
        return redirect('asignar_cirugia', consulta_id=consulta.id)

    if request.method == 'POST':
        form = CirugiaForm(request.POST, instance=cirugia)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Cirugía actualizada correctamente.")
            return redirect('ver_cirugia', consulta_id=consulta.id)
    else:
        form = CirugiaForm(instance=cirugia)

    return render(request, 'principal/formulario_cirugia.html', {
        'form': form,
        'consulta': consulta
    })

def eliminar_cirugia(request, consulta_id):
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    cirugia = getattr(consulta, 'cirugia', None)

    if not cirugia:
        return redirect('detalle_consulta', consulta_id=consulta_id)

    if request.method == 'POST':
        cirugia.delete()
        messages.success(request, "🗑️ Cirugía eliminada correctamente.")
        return redirect('detalle_consulta', consulta_id=consulta_id)

    return render(request, 'principal/confirmar_eliminar.html', {
        'objeto': cirugia,
        'tipo': 'cirugía',
        'consulta': consulta
    })

def lista_cirugias(request):
    cirugias = Cirugia.objects.filter(activo=True).order_by('fecha_prog', 'hora_prog')
    return render(request, 'principal/lista_cirugias.html', {'cirugias': cirugias})

def editar_cirugia_directa(request, cirugia_id):
    cirugia = get_object_or_404(Cirugia, pk=cirugia_id, activo=True)

    if request.method == 'POST':
        form = CirugiaForm(request.POST, instance=cirugia)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Cirugía actualizada correctamente.")
            return redirect('lista_cirugias')
    else:
        form = CirugiaForm(instance=cirugia)

    return render(request, 'principal/formulario_cirugia.html', {
        'form': form,
        'consulta': cirugia.consulta  # puede ser None
    })

def cancelar_cirugia(request, cirugia_id):
    cirugia = get_object_or_404(Cirugia, pk=cirugia_id, activo=True)
    #cirugia.activo = False
    cirugia.estado = 'Cancelada'
    cirugia.save()
    messages.warning(request, "❌ Cirugía cancelada correctamente.")
    return redirect('lista_cirugias')

def cirugia_realizada(request, cirugia_id):
    cirugia = get_object_or_404(Cirugia, pk=cirugia_id, activo=True)
    cirugia.estado = 'Realizada'
    cirugia.save()
    messages.success(request, "✅ Cirugía marcada como realizada correctamente.")
    return redirect('lista_cirugias')

def cirugias_pendientes(request):
    # 1. Cirugías incompletas (ya existen pero les faltan datos clave)
    cirugias_incompletas = Cirugia.objects.filter(
        activo=True
    ).filter(
        Q(procedimiento__isnull=True) | Q(procedimiento='') |
        Q(fecha_prog__isnull=True) |
        Q(hora_prog__isnull=True) |
        Q(profesional__isnull=True)
    )

    # 2. Consultas que requieren cirugía pero aún no la tienen
    consultas_sin_cirugia = Consulta.objects.filter(
        req_cirugia=True
    ).exclude(
        cirugia__isnull=False  # Evita las que ya tienen al menos una cirugía
    )

    return render(request, 'principal/cirugias_pendientes.html', {
        'cirugias': cirugias_incompletas,
        'consultas': consultas_sin_cirugia
    })

def crear_cirugia(request):
    if request.method == 'POST':
        form = CirugiaForm(request.POST)
        if form.is_valid():
            nueva_cirugia = form.save(commit=False)
            nueva_cirugia.estado = 'Programada'
            nueva_cirugia.activo = True
            nueva_cirugia.save()
            messages.success(request, "✅ Cirugía creada correctamente.")
            return redirect('lista_cirugias')
    else:
        form = CirugiaForm()

    return render(request, 'principal/formulario_cirugia.html', {
        'form': form
    })


#Exportar Excel

def exportar_clientes(request):
    clientes = Cliente.objects.all()
    encabezados = ['Nombre', 'Cédula', 'Teléfono', 'Dirección', 'Activo']
    filas = [
        [c.nombre, c.cedula, c.telefono or '', c.direccion or '', 'Sí' if c.activo else 'No']
        for c in clientes
    ]
    return generar_excel("clientes", encabezados, filas)

def exportar_mascotas(request):
    mascotas = Mascota.objects.select_related('cliente')
    encabezados = ['Nombre', 'Especie', 'Raza', 'Edad', 'Dueño', 'Activo']
    filas = [
        [m.nombre_mascota, m.especie, m.raza, m.edad, m.cliente.nombre, 'Sí' if m.activo else 'No']
        for m in mascotas
    ]
    return generar_excel("mascotas", encabezados, filas)

def exportar_consultas(request):
    consultas = Consulta.objects.select_related('mascota', 'mascota__cliente')
    encabezados = ['Fecha', 'Mascota', 'Dueño', 'Motivo', 'Diagnóstico', 'Medicamentos', 'Entregado', 'Cirugía']
    filas = [
        [
            c.fecha,
            c.mascota.nombre_mascota,
            c.mascota.cliente.nombre,
            c.motivo,
            c.diagnostico,
            'Sí' if c.req_medicamentos else 'No',
            'Sí' if c.med_entregado else 'No',
            'Sí' if c.req_cirugia else 'No'
        ] for c in consultas
    ]
    return generar_excel("consultas", encabezados, filas)

def exportar_cirugias(request):
    cirugias = Cirugia.objects.select_related('mascota', 'profesional', 'consulta')
    encabezados = [
        'Mascota', 'Profesional', 'Procedimiento', 'Descripción', 'Fecha', 'Hora',
        'Duración', 'Estado', 'Observaciones', 'Consulta Relacionada', 'Activo'
    ]
    filas = [
        [
            c.mascota.nombre_mascota,
            c.profesional.nombre_prof if c.profesional else '',
            c.procedimiento,
            c.descripcion_proced or '',
            c.fecha_prog,
            c.hora_prog,
            str(c.duracion_aprox),
            c.estado,
            c.observaciones_cirugia or '',
            c.consulta.id if c.consulta else '',
            'Sí' if c.activo else 'No'
        ]
        for c in cirugias
    ]
    return generar_excel("cirugias", encabezados, filas)

def exportar_formulas(request):
    formulas = FormulaMedica.objects.select_related('consulta', 'medicamento')
    encabezados = [
        'Consulta ID', 'Mascota', 'Medicamento', 'Dosis', 'Frecuencia', 'Duración',
        'Vía Administración', 'Observaciones', 'Fecha de Creación'
    ]
    filas = [
        [
            f.consulta.id,
            f.consulta.mascota.nombre_mascota,
            f.medicamento.nombre_med,
            f.dosis,
            f.frecuencia,
            f.duracion,
            f.via_administracion,
            f.observaciones or '',
            f.fecha_creacion.strftime('%Y-%m-%d %H:%M')
        ]
        for f in formulas
    ]
    return generar_excel("formulas_medicas", encabezados, filas)


def exportar_profesionales(request):
    profesionales = Profesional.objects.all()
    encabezados = ['Nombre', 'Tarjeta Profesional', 'Teléfono', 'Especialidad', 'Activo']
    filas = [
        [
            p.nombre_prof,
            p.tarjeta_profesional,
            p.telefono or '',
            p.especialidad or '',
            'Sí' if p.activo else 'No'
        ]
        for p in profesionales
    ]
    return generar_excel("profesionales", encabezados, filas)


def exportar_medicamentos(request):
    medicamentos = Medicamento.objects.all()
    encabezados = ['Nombre', 'Presentación', 'Stock Disponible', 'Fecha de Vencimiento', 'Activo']
    filas = [
        [
            m.nombre_med,
            m.presentacion,
            m.stock_disponible,
            m.fecha_vencimiento,
            'Sí' if m.activo else 'No'
        ]
        for m in medicamentos
    ]
    return generar_excel("medicamentos", encabezados, filas)

