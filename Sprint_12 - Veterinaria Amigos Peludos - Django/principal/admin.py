from django.contrib import admin
from .models import Cliente, Mascota, Consulta, Medicamento, Profesional, Cirugia, FormulaMedica

admin.site.register(Cliente)
admin.site.register(Mascota)
admin.site.register(Consulta)
admin.site.register(Medicamento)
admin.site.register(Profesional)
admin.site.register(Cirugia)
admin.site.register(FormulaMedica)
