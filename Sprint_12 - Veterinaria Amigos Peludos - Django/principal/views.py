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
from .models import Mascota, Consulta
from django.shortcuts import render, get_object_or_404
from datetime import datetime
import logging

# Configuración del logger
logger = logging.getLogger('principal')

# Vista de inicio
def inicio(request):
    try:
        logger.info("🔍 Accediendo a la vista de inicio.")

        cirugias = Cirugia.objects.filter(
            activo=True,
            fecha_prog__gte=date.today()
        ).order_by('fecha_prog', 'hora_prog')[:5]

        logger.info(f"✅ Se encontraron {len(cirugias)} cirugías programadas para mostrar en inicio.")

        return render(request, 'principal/inicio.html', {
            'cirugias': cirugias
        })

    except Exception as e:
        logger.error(f"❌ Error al cargar la vista de inicio: {e}")
        messages.error(request, "Ocurrió un error al cargar la página de inicio.")
        return render(request, 'principal/inicio.html', {'cirugias': []})

def clientes(request):
    return render(request, 'principal/clientes.html')

def mascotas(request):
    return render(request, 'principal/mascotas.html')

#ORM Clientes
def lista_clientes(request):
    try:
        logger.info("📋 Accediendo a la lista de clientes.")

        clientes = Cliente.objects.filter(activo=True)
        logger.info(f"✅ Se encontraron {clientes.count()} clientes activos.")

        return render(request, 'principal/lista_clientes.html', {'clientes': clientes})

    except Exception as e:
        logger.error(f"❌ Error al cargar la lista de clientes: {e}")
        messages.error(request, "Ocurrió un error al cargar la lista de clientes.")
        return render(request, 'principal/lista_clientes.html', {'clientes': []})


def crear_cliente(request):
    try:
        if request.method == 'POST':
            form = ClienteForm(request.POST)
            if form.is_valid():
                cliente = form.save()
                logger.info(f"🆕 Cliente creado: {cliente.nombre} (ID: {cliente.id})")
                messages.success(request, "Cliente creado correctamente.")
                return redirect('lista_clientes')
            else:
                logger.warning("⚠️ Formulario inválido al crear cliente.")
        else:
            form = ClienteForm()
            logger.info("📄 Mostrando formulario para crear cliente.")
    except Exception as e:
        logger.error(f"❌ Error al crear cliente: {e}")
        messages.error(request, "Ocurrió un error al crear el cliente.")
        form = ClienteForm()

    return render(request, 'principal/formulario_cliente.html', {'form': form})


def editar_cliente(request, cedula):
    try:
        cliente = get_object_or_404(Cliente, cedula=cedula)
        if request.method == 'POST':
            form = ClienteForm(request.POST, instance=cliente)
            if form.is_valid():
                form.save()
                logger.info(f"✏️ Cliente editado: {cliente.nombre} (Cédula: {cliente.cedula})")
                messages.success(request, "Cliente editado correctamente.")
                return redirect('lista_clientes')
            else:
                logger.warning(f"⚠️ Formulario inválido al editar cliente {cliente.cedula}.")
        else:
            form = ClienteForm(instance=cliente)
            logger.info(f"📄 Mostrando formulario para editar cliente: {cliente.cedula}")
    except Exception as e:
        logger.error(f"❌ Error al editar cliente con cédula {cedula}: {e}")
        messages.error(request, "Ocurrió un error al editar el cliente.")
        form = ClienteForm()

    return render(request, 'principal/formulario_cliente.html', {'form': form})

def eliminar_cliente(request, cedula):
    try:
        cliente = get_object_or_404(Cliente, cedula=cedula)
        cliente.activo = False
        cliente.save()
        logger.info(f"🗑 Cliente eliminado lógicamente: {cliente.nombre} (Cédula: {cliente.cedula})")
        messages.success(request, f"Cliente '{cliente.nombre}' eliminado correctamente.")
    except Exception as e:
        logger.error(f"❌ Error al eliminar cliente con cédula {cedula}: {e}")
        messages.error(request, "Ocurrió un error al eliminar el cliente.")

    return redirect('lista_clientes')


#ORM Mascotas
def lista_mascotas(request):
    try:
        mascotas = Mascota.objects.filter(activo=True)
        logger.info(f"✅ Se listaron {mascotas.count()} mascotas activas.")
    except Exception as e:
        logger.error(f"❌ Error al obtener la lista de mascotas: {e}")
        mascotas = []
        messages.error(request, "Ocurrió un error al cargar las mascotas.")

    return render(request, 'principal/lista_mascotas.html', {'mascotas': mascotas})

def crear_mascota(request):
    cliente_id = request.GET.get('cliente_id')
    cliente = Cliente.objects.filter(id=cliente_id).first() if cliente_id else None

    try:
        if request.method == 'POST':
            form = MascotaForm(request.POST)
            if form.is_valid():
                mascota = form.save(commit=False)
                if cliente:
                    mascota.cliente = cliente  # aseguramos que no cambien el cliente
                mascota.save()
                logger.info(f"✅ Mascota creada: {mascota.nombre_mascota} (Cliente: {mascota.cliente})")
                messages.success(request, "Mascota registrada correctamente.")
                return redirect('lista_mascotas')
            else:
                logger.warning("⚠️ Formulario inválido al crear mascota.")
        else:
            initial_data = {'cliente': cliente.id} if cliente else {}
            form = MascotaForm(initial=initial_data)
    except Exception as e:
        logger.error(f"❌ Error al crear mascota: {e}")
        messages.error(request, "Ocurrió un error al intentar registrar la mascota.")
        form = MascotaForm()

    return render(request, 'principal/formulario_mascota.html', {
        'form': form,
        'modo': 'Crear',
        'cliente_bloqueado': cliente is not None,
        'cliente': cliente
    })

def editar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    cliente = mascota.cliente  # Obtenemos el cliente actual (dueño)

    try:
        if request.method == 'POST':
            form = MascotaForm(request.POST, instance=mascota)
            if form.is_valid():
                mascota_editada = form.save(commit=False)
                mascota_editada.cliente = cliente  # Evitamos que se cambie el dueño
                mascota_editada.save()
                logger.info(f"✏️ Mascota editada: {mascota_editada.nombre_mascota} (ID: {mascota_editada.id})")
                messages.success(request, "Mascota editada correctamente.")
                return redirect('lista_mascotas')
            else:
                logger.warning(f"⚠️ Formulario inválido al editar la mascota con ID {pk}")
        else:
            form = MascotaForm(instance=mascota)
    except Exception as e:
        logger.error(f"❌ Error al editar mascota (ID: {pk}): {e}")
        messages.error(request, "Ocurrió un error al editar la mascota.")
        form = MascotaForm(instance=mascota)

    return render(request, 'principal/formulario_mascota.html', {
        'form': form,
        'modo': 'Editar',
        'cliente_bloqueado': True,
        'cliente': cliente
    })

def eliminar_mascota(request, pk):
    try:
        mascota = get_object_or_404(Mascota, pk=pk)
        mascota.activo = False
        mascota.save()
        logger.info(f"🗑 Mascota eliminada lógicamente: {mascota.nombre_mascota} (ID: {mascota.id})")
        messages.success(request, "Mascota eliminada correctamente.")
    except Exception as e:
        logger.error(f"❌ Error al eliminar mascota con ID {pk}: {e}")
        messages.error(request, "Ocurrió un error al eliminar la mascota.")

    return redirect('lista_mascotas')


def buscar_clientes(request):
    try:
        q = request.GET.get('q', '').strip().lower()
        coincidencias = Cliente.objects.filter(
            activo=True
        ).filter(
            models.Q(nombre__icontains=q) | models.Q(cedula__icontains=q)
        ).values('id', 'nombre', 'cedula')[:10]

        logger.info(f"🔍 Búsqueda de clientes con query: '{q}' - {coincidencias.count()} resultados.")
        return JsonResponse(list(coincidencias), safe=False)

    except Exception as e:
        logger.error(f"❌ Error en la búsqueda de clientes: {e}")
        return JsonResponse({'error': 'Error interno al buscar clientes'}, status=500)


def mascotas_por_cliente(request, cliente_id):
    try:
        cliente = get_object_or_404(Cliente, id=cliente_id)
        mascotas = Mascota.objects.filter(cliente=cliente, activo=True)
        logger.info(f"📋 Listando mascotas para el cliente: {cliente.nombre} (ID: {cliente.id}) - {mascotas.count()} mascotas.")
        return render(request, 'principal/mascotas_por_cliente.html', {'cliente': cliente, 'mascotas': mascotas})

    except Exception as e:
        logger.error(f"❌ Error al listar mascotas del cliente ID {cliente_id}: {e}")
        messages.error(request, "Ocurrió un error al cargar las mascotas del cliente.")
        return redirect('lista_clientes')

#ORM Consultas
def lista_consultas(request):
    try:
        consultas = Consulta.objects.select_related('mascota').order_by('-fecha')
        logger.info(f"📋 Lista de consultas cargada correctamente. Total: {consultas.count()}")
        return render(request, 'principal/lista_consultas.html', {'consultas': consultas})

    except Exception as e:
        logger.error(f"❌ Error al cargar la lista de consultas: {e}")
        messages.error(request, "Ocurrió un error al cargar las consultas.")
        return redirect('inicio')

def crear_consulta(request):
    try:
        if request.method == 'POST':
            form = ConsultaForm(request.POST)
            if form.is_valid():
                consulta = form.save(commit=False)
                consulta.mascota = form.cleaned_data['mascota']
                consulta.save()
                logger.info(f"✅ Consulta creada correctamente para mascota ID: {consulta.mascota.id}")
                messages.success(request, "Consulta registrada correctamente.")
                return redirect('detalle_consulta', consulta.id)
            else:
                logger.warning("⚠️ Formulario de consulta inválido al crear.")
                messages.warning(request, "Por favor verifica los datos del formulario.")
        else:
            form = ConsultaForm()

        return render(request, 'principal/formulario_consulta.html', {'form': form})

    except Exception as e:
        logger.error(f"❌ Error al crear la consulta: {e}")
        messages.error(request, "Ocurrió un error al registrar la consulta.")
        return redirect('lista_consultas')


def editar_consulta(request, consulta_id):
    try:
        consulta = get_object_or_404(Consulta, pk=consulta_id)

        if request.method == 'POST':
            form = ConsultaForm(request.POST, instance=consulta)
            if form.is_valid():
                consulta = form.save()
                logger.info(f"📝 Consulta editada exitosamente. ID: {consulta.id}")
                messages.success(request, "Consulta actualizada correctamente.")

                # Redirigir a asignación de cirugía si aplica
                if consulta.req_cirugia and not Cirugia.objects.filter(consulta=consulta).exists():
                    logger.info(f"🔁 Redirigiendo a asignación de cirugía para consulta ID: {consulta.id}")
                    return redirect('asignar_cirugia', consulta_id=consulta.id)

                return redirect('detalle_consulta', consulta.id)
            else:
                logger.warning(f"⚠️ Formulario inválido al editar consulta ID: {consulta.id}")
                messages.warning(request, "El formulario contiene errores. Verifica los campos.")
        else:
            form = ConsultaForm(instance=consulta)

        return render(request, 'principal/formulario_consulta.html', {'form': form})

    except Exception as e:
        logger.error(f"❌ Error al editar consulta ID {consulta_id}: {e}")
        messages.error(request, "Ocurrió un error al editar la consulta.")
        return redirect('lista_consultas')

def eliminar_consulta(request, pk):
    try:
        consulta = get_object_or_404(Consulta, pk=pk)
        consulta.delete()
        logger.info(f"🗑 Consulta eliminada exitosamente. ID: {pk}")
        messages.success(request, "Consulta eliminada correctamente.")
    except Exception as e:
        logger.error(f"❌ Error al eliminar la consulta ID {pk}: {e}")
        messages.error(request, "Ocurrió un error al intentar eliminar la consulta.")
    return redirect('lista_consultas')


def detalle_consulta(request, consulta_id):
    try:
        consulta = get_object_or_404(Consulta, id=consulta_id)
        formulas = FormulaMedica.objects.filter(consulta=consulta)

        # Determinar el estado de medicamentos
        if not formulas.exists():
            estado_medicamentos = "pendiente_asignar"
        elif not consulta.med_entregado:
            estado_medicamentos = "pendiente_entregar"
        else:
            estado_medicamentos = "entregado"

        logger.info(f"👁 Vista de detalles de consulta ID {consulta_id} accedida correctamente.")

        context = {
            'consulta': consulta,
            'estado_medicamentos': estado_medicamentos
        }
        return render(request, 'principal/detalle_consulta.html', context)

    except Exception as e:
        logger.error(f"❌ Error al cargar detalles de consulta ID {consulta_id}: {e}")
        messages.error(request, "Ocurrió un error al cargar los detalles de la consulta.")
        return redirect('lista_consultas')

#Historia Clinica
def historia_clinica(request, mascota_id):
    try:
        mascota = get_object_or_404(Mascota, id=mascota_id)
        consultas = mascota.consultas.select_related(
            'mascota', 'mascota__cliente'
        ).prefetch_related(
            'formulas__medicamento', 'cirugia'
        ).order_by('-fecha')

        hora_actual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        logger.info(f"📖 Historia clínica accedida para la mascota ID {mascota_id} - {mascota.nombre_mascota}")

        return render(request, 'principal/historia_clinica.html', {
            'mascota': mascota,
            'consultas': consultas,
            'hora_actual': hora_actual
        })

    except Exception as e:
        logger.error(f"❌ Error al cargar la historia clínica de la mascota ID {mascota_id}: {e}")
        messages.error(request, "Ocurrió un error al cargar la historia clínica.")
        return redirect('lista_mascotas')

def exportar_historia_pdf(request, mascota_id):
    try:
        mascota = get_object_or_404(Mascota, pk=mascota_id)
        consultas = mascota.consultas.all().order_by('-fecha')

        logo_url = request.build_absolute_uri(static('principal/img/logo.png'))

        html_string = render_to_string('principal/historia_clinica_pdf.html', {
            'mascota': mascota,
            'consultas': consultas,
            'logo_url': logo_url
        })

        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf = html.write_pdf()

        logger.info(f"📄 PDF de historia clínica generado para la mascota {mascota.nombre_mascota} (ID {mascota.id})")

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'filename="historia_clinica_{mascota.nombre_mascota}.pdf"'
        return response

    except Exception as e:
        logger.error(f"❌ Error al generar PDF de historia clínica para la mascota ID {mascota_id}: {e}")
        messages.error(request, "Ocurrió un error al generar el PDF de la historia clínica.")
        return redirect('historia_clinica', mascota_id=mascota_id)

def buscar_mascotas(request):
    try:
        q = request.GET.get('q', '').strip()
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

        logger.info(f"🔎 Búsqueda de mascotas realizada con query: '{q}' - {len(data)} resultados encontrados")
        return JsonResponse(data, safe=False)

    except Exception as e:
        logger.error(f"❌ Error en la búsqueda de mascotas con query '{q}': {e}")
        return JsonResponse({'error': 'Error al buscar mascotas.'}, status=500)

#ORM Formula medica
def crear_formula_medica(request, consulta_id):
    try:
        consulta = get_object_or_404(Consulta, pk=consulta_id)
        logger.info(f"🧾 Acceso al formulario de fórmula médica para la consulta ID {consulta_id}")

        if not consulta.req_medicamentos:
            logger.warning(f"⚠️ La consulta ID {consulta_id} no requiere medicamentos. Redirigiendo a detalles.")
            return redirect('detalle_consulta', consulta_id=consulta.id)

        if request.method == 'POST':
            form = FormulaMedicaForm(request.POST)
            if form.is_valid():
                formula = form.save(commit=False)
                formula.consulta = consulta
                formula.save()
                logger.info(f"✅ Fórmula médica creada correctamente para consulta ID {consulta_id}")
                return redirect('detalle_consulta', consulta_id=consulta.id)
            else:
                logger.warning(f"❌ Formulario inválido al crear fórmula médica para consulta ID {consulta_id}")
        else:
            form = FormulaMedicaForm()

        return render(request, 'principal/formula_medica_form.html', {
            'form': form,
            'consulta': consulta
        })

    except Exception as e:
        logger.error(f"🚨 Error al crear fórmula médica para consulta ID {consulta_id}: {e}")
        messages.error(request, "Ocurrió un error al crear la fórmula médica.")
        return redirect('detalle_consulta', consulta_id=consulta_id)

def asignar_medicamentos(request, consulta_id):
    try:
        consulta = get_object_or_404(Consulta, id=consulta_id)
        logger.info(f"🧾 Acceso al formulario de asignación de medicamentos para consulta ID {consulta_id}")

        if consulta.med_entregado:
            logger.warning(f"❌ Intento de asignar medicamentos ya entregados para consulta ID {consulta_id}")
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
                    logger.info(f"➕ Medicamento '{medicamento.nombre_med}' asignado a consulta ID {consulta_id}")
                else:
                    logger.warning(f"⚠️ Medicamento con ID {med_id} no encontrado")

                index += 1

            if accion == 'guardar':
                logger.info(f"💾 {len(formulas)} medicamentos guardados para consulta ID {consulta_id}")
                messages.success(request, f"💾 Fórmula guardada con {len(formulas)} medicamentos.")
                return redirect('detalle_consulta', consulta_id=consulta.id)

            elif accion == 'entregar':
                consulta.med_entregado = True
                consulta.save()
                logger.info(f"🚚 Medicamentos entregados para consulta ID {consulta_id}: {', '.join(formulas)}")
                messages.success(request, f"🚚 Medicamentos entregados: {', '.join(formulas)}")
                return redirect('detalle_consulta', consulta_id=consulta.id)

        return render(request, 'principal/formulario_formula_medica.html', {
            'consulta': consulta,
            'medicamentos': medicamentos,
            'guardado': False
        })

    except Exception as e:
        logger.error(f"❌ Error al asignar medicamentos en consulta ID {consulta_id}: {e}")
        messages.error(request, "Ocurrió un error al asignar medicamentos.")
        return redirect('detalle_consulta', consulta_id=consulta_id)

@csrf_protect
def ver_formula_medica(request, consulta_id):
    try:
        consulta = get_object_or_404(Consulta, id=consulta_id)
        formulas = FormulaMedica.objects.filter(consulta=consulta)

        logger.info(f"[VISITA] Vista de fórmula médica accedida para la consulta ID={consulta_id}")

        if request.method == 'POST' and request.POST.get('accion') == 'entregar':
            if not consulta.med_entregado:
                consulta.med_entregado = True
                consulta.save()
                logger.info(f"[ENTREGA] Medicamentos entregados para consulta ID={consulta.id}")
                messages.success(request, "🚚 Medicamentos marcados como entregados.")
                return redirect('ver_formula', consulta_id=consulta.id)
            else:
                logger.warning(f"[ENTREGA OMITIDA] Ya estaban entregados los medicamentos para consulta ID={consulta.id}")

        return render(request, 'principal/ver_formula_medica.html', {
            'consulta': consulta,
            'formulas': formulas
        })

    except Exception as e:
        logger.error(f"[ERROR] Error al mostrar o procesar fórmula médica para consulta ID={consulta_id}: {str(e)}")
        messages.error(request, "Ocurrió un error al cargar la fórmula médica.")
        return redirect('lista_consultas')

def asignar_cirugia(request, consulta_id):
    try:
        logger.info(f"[VISITA] Vista de asignación de cirugía accedida para consulta ID={consulta_id}")
        return render(request, 'principal/asignar_cirugia.html', {'consulta_id': consulta_id})
    except Exception as e:
        logger.error(f"[ERROR] Error al acceder a asignar_cirugia para consulta ID={consulta_id}: {str(e)}")
        messages.error(request, "Ocurrió un error al cargar la asignación de cirugía.")
        return redirect('lista_consultas')


def lista_formulas(request):
    query = request.GET.get('buscar', '')
    try:
        formulas = Consulta.objects.filter(req_medicamentos=True)

        if query:
            formulas = formulas.filter(
                mascota__nombre_mascota__icontains=query
            ) | formulas.filter(
                mascota__cliente__nombre__icontains=query
            )
            logger.info(f"[BÚSQUEDA] Filtrando fórmulas por query: '{query}'")

        logger.info(f"[VISITA] Vista de lista de fórmulas accedida. Total resultados: {formulas.count()}")

        context = {
            'formulas': formulas,
            'query': query,
        }
        return render(request, 'principal/lista_formulas.html', context)

    except Exception as e:
        logger.error(f"[ERROR] Error en lista_formulas: {str(e)}")
        messages.error(request, "Ocurrió un error al cargar las fórmulas médicas.")
        return redirect('inicio')

def lista_medicamentos(request):
    try:
        medicamentos = Medicamento.objects.filter(activo=True).order_by('nombre_med')
        paginator = Paginator(medicamentos, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        logger.info(f"[VISITA] Lista de medicamentos cargada. Página solicitada: {page_number or 1}, Total: {paginator.count}")

        return render(request, 'principal/lista_medicamentos.html', {
            'page_obj': page_obj
        })

    except Exception as e:
        logger.error(f"[ERROR] Error al listar medicamentos: {str(e)}")
        messages.error(request, "❌ Ocurrió un error al mostrar los medicamentos.")
        return redirect('inicio')

def lista_profesionales(request):
    try:
        profesionales = Profesional.objects.filter(activo=True).order_by('nombre_prof')
        paginator = Paginator(profesionales, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        logger.info(f"[VISITA] Lista de profesionales cargada. Página solicitada: {page_number or 1}, Total: {paginator.count}")

        return render(request, 'principal/lista_profesionales.html', {
            'page_obj': page_obj
        })

    except Exception as e:
        logger.error(f"[ERROR] Error al listar profesionales: {str(e)}")
        messages.error(request, "❌ Ocurrió un error al mostrar los profesionales.")
        return redirect('inicio')

# ORM Medicamentos
def crear_medicamento(request):
    try:
        if request.method == 'POST':
            form = MedicamentoForm(request.POST)
            if form.is_valid():
                medicamento = form.save()
                logger.info(f"[CREACIÓN] Medicamento creado: {medicamento.nombre_med} (ID: {medicamento.id})")
                messages.success(request, "✅ Medicamento creado correctamente.")
                return redirect('lista_medicamentos')
            else:
                logger.warning("[VALIDACIÓN] Error en formulario al crear medicamento.")
        else:
            form = MedicamentoForm()
        return render(request, 'principal/formulario_medicamento.html', {'form': form})

    except Exception as e:
        logger.error(f"[ERROR] al crear medicamento: {str(e)}")
        messages.error(request, "❌ Ocurrió un error al crear el medicamento.")
        return redirect('lista_medicamentos')

def editar_medicamento(request, pk):
    try:
        medicamento = get_object_or_404(Medicamento, pk=pk)
        if request.method == 'POST':
            form = MedicamentoForm(request.POST, instance=medicamento)
            if form.is_valid():
                form.save()
                logger.info(f"[EDICIÓN] Medicamento editado: {medicamento.nombre_med} (ID: {medicamento.id})")
                messages.success(request, "✅ Medicamento actualizado correctamente.")
                return redirect('lista_medicamentos')
            else:
                logger.warning(f"[VALIDACIÓN] Formulario inválido al editar medicamento (ID: {medicamento.id})")
        else:
            form = MedicamentoForm(instance=medicamento)

        return render(request, 'principal/formulario_medicamento.html', {'form': form})

    except Exception as e:
        logger.error(f"[ERROR] al editar medicamento (ID: {pk}): {str(e)}")
        messages.error(request, "❌ Error al intentar editar el medicamento.")
        return redirect('lista_medicamentos')

def eliminar_medicamento(request, pk):
    try:
        medicamento = get_object_or_404(Medicamento, pk=pk)
        medicamento.activo = False
        medicamento.save()
        logger.info(f"[ELIMINACIÓN] Medicamento eliminado: {medicamento.nombre_med} (ID: {medicamento.id}))")
        messages.success(request, "✅ Medicamento eliminado correctamente.")
        return redirect('lista_medicamentos')

    except Exception as e:
        logger.error(f"[ERROR] al eliminar medicamento (ID: {pk}): {str(e)}")
        messages.error(request, "❌ Error al intentar eliminar el medicamento.")
        return redirect('lista_medicamentos')

# ORM Profesional
def editar_profesional(request, pk):
    try:
        profesional = get_object_or_404(Profesional, pk=pk)

        if request.method == 'POST':
            form = ProfesionalForm(request.POST, instance=profesional)
            if form.is_valid():
                form.save()
                logger.info(f"[EDICIÓN] Profesional editado: {profesional.nombre_prof} (ID: {pk})")
                messages.success(request, "✅ Profesional actualizado correctamente.")
                return redirect('lista_profesionales')
        else:
            form = ProfesionalForm(instance=profesional)

        return render(request, 'principal/formulario_profesional.html', {'form': form})

    except Exception as e:
        logger.error(f"[ERROR] al editar profesional (ID: {pk}): {str(e)}")
        messages.error(request, "❌ Error al intentar editar al profesional.")
        return redirect('lista_profesionales')

def eliminar_profesional(request, pk):
    try:
        profesional = get_object_or_404(Profesional, pk=pk)
        profesional.activo = False 
        profesional.save()
        logger.info(f"[ELIMINACIÓN] Profesional eliminado: {profesional.nombre_prof} (ID: {pk})")
        messages.success(request, f"✅ Profesional '{profesional.nombre_prof}' eliminado correctamente.")
        return redirect('lista_profesionales')

    except Exception as e:
        logger.error(f"[ERROR] al eliminar profesional (ID: {pk}): {str(e)}")
        messages.error(request, "❌ Error al intentar eliminar al profesional.")
        return redirect('lista_profesionales')

def crear_profesional(request):
    try:
        if request.method == 'POST':
            form = ProfesionalForm(request.POST)
            if form.is_valid():
                profesional = form.save()
                logger.info(f"[CREACIÓN] Profesional creado: {profesional.nombre_prof} (ID: {profesional.id})")
                messages.success(request, f"✅ Profesional '{profesional.nombre_prof}' registrado con éxito.")
                return redirect('lista_profesionales')
        else:
            form = ProfesionalForm()

        return render(request, 'principal/formulario_profesional.html', {'form': form})

    except Exception as e:
        logger.error(f"[ERROR] al crear profesional: {str(e)}")
        messages.error(request, "❌ Ocurrió un error al registrar el profesional.")
        return redirect('lista_profesionales')

# ORM Cirugías
def historial_cirugias(request, pk):
    return HttpResponse("🔧 Módulo de cirugías en construcción.")

def asignar_cirugia(request, consulta_id):
    try:
        consulta = get_object_or_404(Consulta, pk=consulta_id)
        logger.info(f"[ACCESO] Vista de asignación de cirugía para consulta ID {consulta_id}")

        if Cirugia.objects.filter(consulta=consulta).exists():
            logger.warning(f"[IGNORADO] Ya existe cirugía para la consulta ID {consulta_id}")
            return redirect('detalle_consulta', consulta_id=consulta.id)

        if request.method == 'POST':
            form = CirugiaForm(request.POST)
            if form.is_valid():
                cirugia = form.save(commit=False)
                cirugia.mascota = consulta.mascota
                cirugia.consulta = consulta
                cirugia.estado = "Programada"
                cirugia.save()
                logger.info(f"[CREACIÓN] Cirugía programada para consulta ID {consulta.id} (cirugía ID {cirugia.id})")
                messages.success(request, "✅ Cirugía programada correctamente.")
                return redirect('detalle_consulta', consulta.id)
            else:
                logger.warning(f"[FORMULARIO INVÁLIDO] al asignar cirugía para consulta ID {consulta.id}")
        else:
            form = CirugiaForm()

        return render(request, 'principal/formulario_cirugia.html', {
            'form': form,
            'consulta': consulta
        })

    except Exception as e:
        logger.error(f"[ERROR] en asignar_cirugia (consulta ID {consulta_id}): {str(e)}")
        messages.error(request, "❌ Ocurrió un error al intentar programar la cirugía.")
        return redirect('detalle_consulta', consulta_id=consulta_id)

def ver_cirugia(request, consulta_id):
    try:
        consulta = get_object_or_404(Consulta, pk=consulta_id)
        logger.info(f"[ACCESO] Vista de ver cirugía para consulta ID {consulta_id}")

        cirugia = Cirugia.objects.filter(consulta=consulta).first()

        if not cirugia:
            logger.warning(f"[SIN CIRUGÍA] No se encontró una cirugía asociada a la consulta ID {consulta_id}")
            messages.info(request, "ℹ️ No se encontró una cirugía registrada.")
            return redirect('asignar_cirugia', consulta_id=consulta.id)

        logger.info(f"[DETALLE] Mostrando cirugía ID {cirugia.id} para consulta ID {consulta_id}")
        return render(request, 'principal/ver_cirugia.html', {
            'consulta': consulta,
            'cirugia': cirugia
        })

    except Exception as e:
        logger.error(f"[ERROR] en ver_cirugia (consulta ID {consulta_id}): {str(e)}")
        messages.error(request, "❌ Error al intentar mostrar los detalles de la cirugía.")
        return redirect('detalle_consulta', consulta_id=consulta_id)

def editar_cirugia(request, consulta_id):
    try:
        consulta = get_object_or_404(Consulta, pk=consulta_id)
        logger.info(f"[ACCESO] Editar cirugía para consulta ID {consulta_id}")

        cirugia = consulta.cirugia.first()

        if not cirugia:
            logger.warning(f"[SIN CIRUGÍA] No hay cirugía registrada para la consulta ID {consulta_id}")
            messages.warning(request, "No hay una cirugía programada para esta consulta.")
            return redirect('asignar_cirugia', consulta_id=consulta.id)

        if request.method == 'POST':
            form = CirugiaForm(request.POST, instance=cirugia)
            if form.is_valid():
                form.save()
                logger.info(f"[ACTUALIZACIÓN] Cirugía ID {cirugia.id} actualizada correctamente.")
                messages.success(request, "✅ Cirugía actualizada correctamente.")
                return redirect('ver_cirugia', consulta_id=consulta.id)
        else:
            form = CirugiaForm(instance=cirugia)

        return render(request, 'principal/formulario_cirugia.html', {
            'form': form,
            'consulta': consulta
        })

    except Exception as e:
        logger.error(f"[ERROR] al editar cirugía de la consulta ID {consulta_id}: {str(e)}")
        messages.error(request, "❌ Error al intentar editar la cirugía.")
        return redirect('detalle_consulta', consulta_id=consulta_id)

def eliminar_cirugia(request, consulta_id):
    try:
        consulta = get_object_or_404(Consulta, pk=consulta_id)
        cirugia = consulta.cirugia.first()

        if cirugia:
            cirugia.delete()
            logger.info(f"[ELIMINACIÓN] Cirugía eliminada para consulta ID {consulta_id}")
            messages.success(request, "🗑️ Cirugía eliminada correctamente.")
        else:
            logger.warning(f"[NO ENCONTRADA] No se encontró cirugía para consulta ID {consulta_id}")

        return redirect('detalle_consulta', consulta_id=consulta_id)

    except Exception as e:
        logger.error(f"[ERROR] al eliminar cirugía para consulta ID {consulta_id}: {str(e)}")
        messages.error(request, "❌ Error al intentar eliminar la cirugía.")
        return redirect('detalle_consulta', consulta_id=consulta_id)

def lista_cirugias(request):
    try:
        cirugias = Cirugia.objects.filter(activo=True).order_by('fecha_prog', 'hora_prog')
        logger.info(f"[ACCESO] Vista de lista de cirugías accedida por {request.user}. Total: {cirugias.count()}")
        return render(request, 'principal/lista_cirugias.html', {'cirugias': cirugias})
    except Exception as e:
        logger.error(f"[ERROR] al cargar lista de cirugías: {str(e)}")
        messages.error(request, "❌ Ocurrió un error al cargar las cirugías.")
        return redirect('inicio')

def editar_cirugia_directa(request, cirugia_id):
    try:
        cirugia = get_object_or_404(Cirugia, pk=cirugia_id, activo=True)
        logger.info(f"[ACCESO] Edición directa de cirugía (ID: {cirugia_id}) accedida por {request.user}.")

        if request.method == 'POST':
            form = CirugiaForm(request.POST, instance=cirugia)
            if form.is_valid():
                form.save()
                logger.info(f"[ACTUALIZACIÓN] Cirugía actualizada exitosamente (ID: {cirugia_id}) por {request.user}.")
                messages.success(request, "✅ Cirugía actualizada correctamente.")
                return redirect('lista_cirugias')
        else:
            form = CirugiaForm(instance=cirugia)

        return render(request, 'principal/formulario_cirugia.html', {
            'form': form,
            'consulta': cirugia.consulta  # puede ser None
        })

    except Exception as e:
        logger.error(f"[ERROR] al editar cirugía (ID: {cirugia_id}): {str(e)}")
        messages.error(request, "❌ Ocurrió un error al intentar editar la cirugía.")
        return redirect('lista_cirugias')

def cancelar_cirugia(request, cirugia_id):
    try:
        cirugia = get_object_or_404(Cirugia, pk=cirugia_id, activo=True)
        estado_anterior = cirugia.estado
        cirugia.estado = 'Cancelada'
        cirugia.save()

        logger.info(f"[CANCELACIÓN] Cirugía ID {cirugia_id} cambiada de estado '{estado_anterior}' a 'Cancelada' por {request.user}.")
        messages.warning(request, "❌ Cirugía cancelada correctamente.")
        return redirect('lista_cirugias')

    except Exception as e:
        logger.error(f"[ERROR] al cancelar cirugía ID {cirugia_id}: {str(e)}")
        messages.error(request, "❌ Error al intentar cancelar la cirugía.")
        return redirect('lista_cirugias')

def cirugia_realizada(request, cirugia_id):
    try:
        cirugia = get_object_or_404(Cirugia, pk=cirugia_id, activo=True)
        estado_anterior = cirugia.estado
        cirugia.estado = 'Realizada'
        cirugia.save()

        logger.info(f"[ACTUALIZACIÓN] Cirugía ID {cirugia_id} marcada como 'Realizada' (antes: '{estado_anterior}') por {request.user}.")
        messages.success(request, "✅ Cirugía marcada como realizada correctamente.")
        return redirect('lista_cirugias')

    except Exception as e:
        logger.error(f"[ERROR] al marcar cirugía ID {cirugia_id} como realizada: {str(e)}")
        messages.error(request, "❌ Error al marcar la cirugía como realizada.")
        return redirect('lista_cirugias')

def cirugias_pendientes(request):
    try:
        # 1. Cirugías incompletas (campos clave vacíos o nulos)
        cirugias_incompletas = Cirugia.objects.filter(
            activo=True
        ).filter(
            Q(procedimiento__isnull=True) | Q(procedimiento='') |
            Q(fecha_prog__isnull=True) |
            Q(hora_prog__isnull=True) |
            Q(profesional__isnull=True)
        )

        # 2. Consultas que requieren cirugía pero no la tienen asignada
        consultas_sin_cirugia = Consulta.objects.filter(
            req_cirugia=True
        ).exclude(
            cirugia__isnull=False
        )

        logger.info(f"[CONSULTA] Vista de cirugías pendientes accedida por {request.user}. "
                    f"Incompletas: {cirugias_incompletas.count()}, Sin asignar: {consultas_sin_cirugia.count()}")

        return render(request, 'principal/cirugias_pendientes.html', {
            'cirugias': cirugias_incompletas,
            'consultas': consultas_sin_cirugia
        })

    except Exception as e:
        logger.error(f"[ERROR] al cargar cirugías pendientes: {str(e)}")
        messages.error(request, "❌ Error al mostrar las cirugías pendientes.")
        return redirect('inicio')

def crear_cirugia(request):
    try:
        if request.method == 'POST':
            form = CirugiaForm(request.POST)
            if form.is_valid():
                nueva_cirugia = form.save(commit=False)
                nueva_cirugia.estado = 'Programada'
                nueva_cirugia.activo = True
                nueva_cirugia.save()
                logger.info(f"[CREACIÓN] Cirugía programada para mascota '{nueva_cirugia.mascota}' "
                            f"el {nueva_cirugia.fecha_prog} a las {nueva_cirugia.hora_prog}")
                messages.success(request, "✅ Cirugía creada correctamente.")
                return redirect('lista_cirugias')
        else:
            form = CirugiaForm()

        return render(request, 'principal/formulario_cirugia.html', {
            'form': form
        })

    except Exception as e:
        logger.error(f"[ERROR] al crear cirugía: {str(e)}")
        messages.error(request, "❌ Hubo un error al crear la cirugía.")
        return redirect('lista_cirugias')

#Exportar a CSV
def exportar_clientes(request):
    try:
        clientes = Cliente.objects.all()
        encabezados = ['Nombre', 'Cédula', 'Teléfono', 'Dirección', 'Activo']
        filas = [
            [c.nombre, c.cedula, c.telefono or '', c.direccion or '', 'Sí' if c.activo else 'No']
            for c in clientes
        ]

        logger.info(f"[EXPORTACIÓN] Se exportaron {len(clientes)} clientes a Excel.")
        return generar_excel("clientes", encabezados, filas)

    except Exception as e:
        logger.error(f"[ERROR] al exportar clientes: {str(e)}")
        messages.error(request, "❌ Ocurrió un error al exportar los clientes.")
        return redirect('lista_clientes')

def exportar_mascotas(request):
    try:
        mascotas = Mascota.objects.select_related('cliente')
        encabezados = ['Nombre', 'Especie', 'Raza', 'Edad', 'Dueño', 'Activo']
        filas = [
            [m.nombre_mascota, m.especie, m.raza, m.edad, m.cliente.nombre, 'Sí' if m.activo else 'No']
            for m in mascotas
        ]

        logger.info(f"[EXPORTACIÓN] Se exportaron {len(mascotas)} mascotas a Excel.")
        return generar_excel("mascotas", encabezados, filas)

    except Exception as e:
        logger.error(f"[ERROR] al exportar mascotas: {str(e)}")
        messages.error(request, "❌ Ocurrió un error al exportar las mascotas.")
        return redirect('lista_mascotas')

def exportar_consultas(request):
    try:
        consultas = Consulta.objects.select_related('mascota', 'mascota__cliente')
        encabezados = ['Fecha', 'Mascota', 'Dueño', 'Motivo', 'Diagnóstico', 'Medicamentos', 'Entregado', 'Cirugía']
        filas = [
            [
                c.fecha,
                c.mascota.nombre_mascota,
                c.mascota.cliente.nombre,
                c.motivo or '',
                c.diagnostico or '',
                'Sí' if c.req_medicamentos else 'No',
                'Sí' if c.med_entregado else 'No',
                'Sí' if c.req_cirugia else 'No'
            ]
            for c in consultas
        ]

        logger.info(f"[EXPORTACIÓN] {len(consultas)} consultas exportadas a Excel.")
        return generar_excel("consultas", encabezados, filas)

    except Exception as e:
        logger.error(f"[ERROR] al exportar consultas: {str(e)}")
        messages.error(request, "❌ Ocurrió un error al exportar las consultas.")
        return redirect('lista_consultas')

def exportar_cirugias(request):
    try:
        cirugias = Cirugia.objects.select_related('mascota', 'profesional', 'consulta')
        encabezados = [
            'Mascota', 'Profesional', 'Procedimiento', 'Descripción', 'Fecha', 'Hora',
            'Duración', 'Estado', 'Observaciones', 'Consulta Relacionada', 'Activo'
        ]

        filas = [
            [
                c.mascota.nombre_mascota,
                c.profesional.nombre_prof if c.profesional else '',
                c.procedimiento or '',
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

        logger.info(f"[EXPORTACIÓN] {len(cirugias)} cirugías exportadas a Excel.")
        return generar_excel("cirugias", encabezados, filas)

    except Exception as e:
        logger.error(f"[ERROR] al exportar cirugías: {str(e)}")
        messages.error(request, "❌ Ocurrió un error al exportar las cirugías.")
        return redirect('lista_cirugias')

def exportar_formulas(request):
    try:
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

        logger.info(f"[EXPORTACIÓN] {len(formulas)} fórmulas médicas exportadas a Excel.")
        return generar_excel("formulas_medicas", encabezados, filas)

    except Exception as e:
        logger.error(f"[ERROR] al exportar fórmulas médicas: {str(e)}")
        messages.error(request, "❌ Error al exportar las fórmulas médicas.")
        return redirect('lista_formulas')

def exportar_profesionales(request):
    try:
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

        logger.info(f"[EXPORTACIÓN] {len(profesionales)} profesionales exportados a Excel.")
        return generar_excel("profesionales", encabezados, filas)

    except Exception as e:
        logger.error(f"[ERROR] al exportar profesionales: {str(e)}")
        messages.error(request, "❌ Error al exportar los profesionales.")
        return redirect('lista_profesionales')

def exportar_medicamentos(request):
    try:
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

        logger.info(f"[EXPORTACIÓN] {len(medicamentos)} medicamentos exportados a Excel.")
        return generar_excel("medicamentos", encabezados, filas)

    except Exception as e:
        logger.error(f"[ERROR] al exportar medicamentos: {str(e)}")
        messages.error(request, "❌ Error al exportar los medicamentos.")
        return redirect('lista_medicamentos')


