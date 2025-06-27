from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('mascotas/', views.mascotas, name='mascotas'),
    path('clientes/', views.clientes, name='clientes'),

     # CRUD de clientes
    path('clientes/lista/', views.lista_clientes, name='lista_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<str:cedula>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<str:cedula>/', views.eliminar_cliente, name='eliminar_cliente'),
    

    # CRUD de mascotas
    path('mascotas/lista/', views.lista_mascotas, name='lista_mascotas'),
    path('mascotas/nueva/', views.crear_mascota, name='crear_mascota'),
    path('mascotas/editar/<int:pk>/', views.editar_mascota, name='editar_mascota'),
    path('mascotas/eliminar/<int:pk>/', views.eliminar_mascota, name='eliminar_mascota'),
    path('buscar_clientes/', views.buscar_clientes, name='buscar_cliente'),

    path('clientes/<int:cliente_id>/mascotas/', views.mascotas_por_cliente, name='mascotas_por_cliente'),

    # CRUD de consultas
    path('consultas/lista/', views.lista_consultas, name='lista_consultas'),
    path('consultas/nueva/', views.crear_consulta_general, name='crear_consulta_general'),
    path('consultas/nueva/<int:mascota_id>/', views.crear_consulta, name='crear_consulta'),
    path('consultas/editar/<int:consulta_id>/', views.editar_consulta, name='editar_consulta'),
    path('consultas/eliminar/<int:pk>/', views.eliminar_consulta, name='eliminar_consulta'),
    path('mascotas/<int:mascota_id>/historia/', views.historia_clinica, name='historia_clinica'),
    path('mascotas/<int:mascota_id>/historia/pdf/', views.exportar_historia_pdf, name='exportar_historia_pdf'),
    path('buscar_mascotas/', views.buscar_mascotas, name='buscar_mascotas'),
    path('consultas/detalle/<int:consulta_id>/', views.detalle_consulta, name='detalle_consulta'),
    path('consultas/<int:consulta_id>/formula/', views.crear_formula_medica, name='crear_formula_medica'),
    path('consulta/<int:consulta_id>/asignar_medicamentos/', views.asignar_medicamentos, name='asignar_medicamentos'),
    path('consulta/<int:consulta_id>/asignar_medicamentos/', views.asignar_medicamentos, name='asignar_medicamentos'),
    path('consulta/<int:consulta_id>/asignar_cirugia/', views.asignar_cirugia, name='asignar_cirugia'),
    path('consulta/<int:consulta_id>/asignar_medicamentos/', views.asignar_medicamentos, name='asignar_medicamentos'),
    #path('consulta/<int:consulta_id>/ver_formula/', views.ver_formula_medica, name='ver_formula_medica'),
    path('consulta/<int:consulta_id>/ver_formula/', views.ver_formula_medica, name='ver_formula'),

    path('formulas/', views.lista_formulas, name='lista_formulas'),

    
    path('medicamentos/', views.lista_medicamentos, name='lista_medicamentos'),
    path('medicamentos/crear/', views.crear_medicamento, name='crear_medicamento'),
    path('medicamentos/editar/<int:pk>/', views.editar_medicamento, name='editar_medicamento'),
    path('medicamentos/eliminar/<int:pk>/', views.eliminar_medicamento, name='eliminar_medicamento'),

    # PROFESIONALES
    path('profesionales/', views.lista_profesionales, name='lista_profesionales'),
    path('profesionales/crear/', views.crear_profesional, name='crear_profesional'),
    path('profesionales/editar/<int:pk>/', views.editar_profesional, name='editar_profesional'),
    path('profesionales/eliminar/<int:pk>/', views.eliminar_profesional, name='eliminar_profesional'),
    path('profesionales/<int:pk>/cirugias/', views.historial_cirugias, name='historial_cirugias'),

    # CRUD CIRUGIAS
    path('consulta/<int:consulta_id>/asignar_cirugia/', views.asignar_cirugia, name='asignar_cirugia'),
    path('consulta/<int:consulta_id>/ver_cirugia/', views.ver_cirugia, name='ver_cirugia'),
    path('consulta/<int:consulta_id>/editar_cirugia/', views.editar_cirugia, name='editar_cirugia'),
    path('consulta/<int:consulta_id>/eliminar_cirugia/', views.eliminar_cirugia, name='eliminar_cirugia'),
    path('cirugias/', views.lista_cirugias, name='lista_cirugias'),
    path('cirugias/editar/<int:cirugia_id>/', views.editar_cirugia_directa, name='editar_cirugia_directa'),
    path('cirugias/cancelar/<int:cirugia_id>/', views.cancelar_cirugia, name='cancelar_cirugia'),
    path('cirugias/realizar/<int:cirugia_id>/', views.cirugia_realizada, name='cirugia_realizada'),
    path('cirugias/pendientes/', views.cirugias_pendientes, name='cirugias_pendientes'),
    path('cirugias/nueva/', views.crear_cirugia, name='crear_cirugia'),

    #EXPORTAR EXCEL
    path('exportar/clientes/', views.exportar_clientes, name='exportar_clientes'),
    path('exportar/mascotas/', views.exportar_mascotas, name='exportar_mascotas'),
    path('exportar/consultas/', views.exportar_consultas, name='exportar_consultas'),
    path('exportar/cirugias/', views.exportar_cirugias, name='exportar_cirugias'),
    path('exportar/formulas/', views.exportar_formulas, name='exportar_formulas'),
    path('exportar/profesionales/', views.exportar_profesionales, name='exportar_profesionales'),
    path('exportar/medicamentos/', views.exportar_medicamentos, name='exportar_medicamentos'),





 





]
