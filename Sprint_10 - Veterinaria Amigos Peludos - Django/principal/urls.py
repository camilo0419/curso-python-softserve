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
]
