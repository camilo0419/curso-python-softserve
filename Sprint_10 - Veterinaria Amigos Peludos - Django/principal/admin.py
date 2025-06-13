from django.contrib import admin
from .models import Cliente, Mascota, Consulta #

# Register your models here.
admin.site.register(Cliente) # Registra el modelo Cliente
admin.site.register(Mascota) # Registra el modelo Mascota
admin.site.register(Consulta) # Registra el modelo Consulta

# Usar python manage.py createsuperuser para crear usuario y administrador
# con python manage.py runserver, accederemos al panel de admin e interacturemos con los datos