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
    path('consultas/nueva/', views.crear_consulta, name='crear_consulta'),
    path('consultas/editar/<int:pk>/', views.editar_consulta, name='editar_consulta'),
    path('consultas/eliminar/<int:pk>/', views.eliminar_consulta, name='eliminar_consulta'),

    path('mascotas/<int:mascota_id>/historia/', views.historia_clinica, name='historia_clinica'),
    path('mascotas/<int:mascota_id>/historia/pdf/', views.exportar_historia_pdf, name='exportar_historia_pdf'),

    path('buscar_mascotas/', views.buscar_mascotas, name='buscar_mascotas'),
    





]
